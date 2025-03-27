import json
import queue
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import io
import asyncio
import time
# from piper import PiperVoice
from celery import Celery, chain, shared_task

from django.contrib.auth.models import User

from asgiref.sync import sync_to_async, async_to_sync

from ai_agent.models import ChatMedia, ChatRoom, Chat, Task, TaskWorkflow

from ai_agent.utils import classify_intent, conversation_assist, convert_prompt_to_json, function_response_to_chat, generate_ai_response, generate_chat_response, process_json_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a Celery instance
app = Celery('conversation_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# # Optimized TTS utilities
# def text_to_speech(text, voice):
#     try:
#         audio = voice.synthesize(text)
#         return audio
#     except Exception as e:
#         logger.error(f"Piper TTS error: {str(e)}")
#         return None

# # Optimized TTS utilities
# def text_to_speech(text, voice):
#     try:
#         audio = voice.synthesize(text)
#         return audio
#     except Exception as e:
#         logger.error(f"GTTS error: {str(e)}")
#         return None

# # Optimized STT utilities
# def speech_to_text(audio_data, recognizer):
#     try:
#         if recognizer.AcceptWaveform(audio_data):
#             result = json.loads(recognizer.Result())
#             return result.get("text", "")
#         else:
#             partial = json.loads(recognizer.PartialResult())
#             return partial.get("partial", "")
#     except Exception as e:
#         logger.error(f"Vosk STT error: {str(e)}")
#         return ""



# class ConversationConsumer(AsyncWebsocketConsumer):
#     vosk_model = Model("C:/Users/USER/OneDrive/Desktop/PROJECTS/AI-Agent-Assistant/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")  # Replace with actual path

#     async def connect(self):
#         await self.accept()
#         self.vosk_rec = KaldiRecognizer(self.vosk_model, 16000)
#         self.audio_queue = queue.Queue()
#         self.transcription_buffer = ""  # Buffer for accumulating transcriptions
#         self.last_transcription_time = time.time()  # Track last update
#         self.silence_threshold = 2  # Seconds of silence to trigger response
#         logger.info(f"WebSocket connected: {self.channel_name}")

#     async def disconnect(self, close_code):
#         logger.info(f"WebSocket disconnected: {self.channel_name} (code: {close_code})")

#     async def receive(self, text_data=None, bytes_data=None):
#         if bytes_data:
#             if self.vosk_rec.AcceptWaveform(bytes_data):
#                 result = json.loads(self.vosk_rec.Result())
#                 transcription = result.get("text", "")
#                 if transcription:
#                     self.transcription_buffer += transcription + " "
#                     self.last_transcription_time = time.time()
#             else:
#                 partial = json.loads(self.vosk_rec.PartialResult())
#                 partial_text = partial.get("partial", "")
#                 await self.send(text_data=json.dumps({"type": "partial", "text": partial_text}))

#             # Check for silence and process if user stopped speaking
#             if time.time() - self.last_transcription_time > self.silence_threshold and self.transcription_buffer:
#                 loop = asyncio.get_event_loop()
#                 loop.run_in_executor(None, self.process_response, self.transcription_buffer.strip())
#                 self.transcription_buffer = ""  # Reset buffer

#         try:
#             while True:
#                 audio_chunk = self.audio_queue.get_nowait()
#                 await self.send(bytes_data=audio_chunk)
#         except queue.Empty:
#             pass

#     def process_response(self, transcription):
#         response = generate_ai_response(transcription)
#         logger.info(f"Transcription: {transcription}")
#         logger.info(f"AI Response: {response}")
#         if not response.startswith("AI error"):
#             # Use gTTS for text-to-speech
#             tts = gTTS(response, lang='en', tld='co.uk')
#             audio_fp = io.BytesIO()
#             tts.write_to_fp(audio_fp)
#             audio_fp.seek(0)
#             audio = audio_fp.read()
#             self.audio_queue.put(audio)
#         else:
#             logger.error(response)


# WebSocket Consumer integrating all functions
# class ConversationConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.vosk_model = Model("path/to/vosk/model")  # Replace with actual path
#         self.vosk_rec = KaldiRecognizer(self.vosk_model, 16000)
#         self.piper_voice = PiperVoice.load("path/to/piper/model")  # Replace with actual path

#     async def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = f'chat_{self.room_id}'
#         self.user = self.scope["user"]
#         self.username = self.user.username
#         # # Join room group
#         # await self.channel_layer.group_add( # type: ignore
#         #     self.room_group_name,
#         #     self.channel_name
#         # )
#         await self.accept()
#         self.audio_queue = queue.Queue()
#         self.transcription_buffer = ""
#         self.last_transcription_time = time.time()
#         self.silence_threshold = 2
#         logger.info(f"WebSocket connected: {self.channel_name}")

#     async def disconnect(self, close_code):
#         logger.info(f"WebSocket disconnected: {self.channel_name} (code: {close_code})")

#     async def receive(self, text_data=None, bytes_data=None):
#         if bytes_data:
#             transcription = speech_to_text(bytes_data, self.vosk_rec)
#             if transcription:
#                 self.transcription_buffer += transcription + " "
#                 self.last_transcription_time = time.time()
#                 await self.send(text_data=json.dumps({"type": "partial", "text": transcription}))

#             if (time.time() - self.last_transcription_time > self.silence_threshold and 
#                 self.transcription_buffer):
#                 prompt = self.transcription_buffer.strip()
#                 self.transcription_buffer = ""

#                 # Step 1: Reassure the user
#                 assist_response = conversation_assist(prompt)
#                 assist_audio = text_to_speech(assist_response, self.piper_voice)
#                 if assist_audio:
#                     self.audio_queue.put(assist_audio)

#                 # Step 2: Convert prompt to JSON
#                 json_response = convert_prompt_to_json(prompt)

#                 # Step 3: Process JSON and execute tasks
#                 result = process_json_response(self.username, self.room_id, json_response)

#                 # Step 4: Summarize results conversationally
#                 chat_response = function_response_to_chat(result)
#                 chat_audio = text_to_speech(chat_response, self.piper_voice)
#                 if chat_audio:
#                     self.audio_queue.put(chat_audio)

#         try:
#             while True:
#                 audio_chunk = self.audio_queue.get_nowait()
#                 await self.send(bytes_data=audio_chunk)
#         except queue.Empty:
#             pass




# Utility function for text-to-speech using gTTS
def text_to_speech(text, lang='en', tld='co.uk'):
    """
    Convert text to speech audio bytes using gTTS.
    """
    tts = gTTS(text, lang=lang, tld=tld)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp.read()

# Utility function for speech-to-text using Vosk
def speech_to_text(recognizer, audio_bytes):
    """
    Process audio bytes with the Vosk recognizer.
    Returns a tuple (transcription, is_final) where:
    - transcription: recognized text (final or partial)
    - is_final: True if the recognizer accepted the waveform, else False.
    """
    if recognizer.AcceptWaveform(audio_bytes):
        result = json.loads(recognizer.Result())
        return result.get("text", ""), True
    else:
        partial = json.loads(recognizer.PartialResult())
        return partial.get("partial", ""), False

class ConversationConsumer(AsyncWebsocketConsumer):
    # Load the Vosk model (ensure the path is correct)
    vosk_model = Model("C:/Users/USER/OneDrive/Desktop/PROJECTS/AI-Agent-Assistant/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")

    async def connect(self):
        self.user = self.scope["user"]
        self.username = self.user.username
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        await self.accept()
        self.vosk_rec = KaldiRecognizer(self.vosk_model, 16000)
        self.audio_queue = queue.Queue()
        self.transcription_buffer = ""  # Buffer for accumulating transcriptions
        self.last_transcription_time = time.time()  # Track the time of the last transcription update
        self.silence_threshold = 2  # Seconds of silence to trigger response
        self.processing_response = False  # Flag to prevent overlapping responses
        logger.info(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {self.channel_name} (code: {close_code})")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Use the speech_to_text utility to process incoming audio bytes
            transcription, is_final = speech_to_text(self.vosk_rec, bytes_data)
            if is_final:
                if transcription:
                    # Append the final transcription to the buffer and update the timestamp
                    self.transcription_buffer += transcription + " "
                    self.last_transcription_time = time.time()
            else:
                # If it's a partial result, send it immediately to the client
                await self.send(text_data=json.dumps({"type": "partial", "text": transcription}))

            # Check if there is silence long enough to trigger processing the accumulated transcription
            if (time.time() - self.last_transcription_time > self.silence_threshold and 
                self.transcription_buffer and not self.processing_response):
                # Set the flag to avoid overlapping responses
                self.processing_response = True
                loop = asyncio.get_event_loop()

                # Text prompt
                prompt = self.transcription_buffer.strip()

                self.transcription_buffer = ""  # Reset the transcription buffer

                # Save user input
                await self.save_msg(self.room_id, prompt, self.username)

                # Classify intent
                intent = classify_intent(prompt)

                if intent == 'task':

                    # Step 1: Reassure the user
                    assist_response = conversation_assist(prompt)

                    # Run process_response asynchronously
                    loop.run_in_executor(None, self.process_response, prompt, assist_response)


                    # Step 2: Convert prompt to JSON
                    json_response = convert_prompt_to_json(prompt)


                    # Display the json
                    logger.info(f"JSON Response: {json_response}")#---------------

                    from asgiref.sync import sync_to_async
                    # Step 3: Process JSON and execute tasks
                    result = await sync_to_async(process_json_response)(self.username, self.room_id, json_response)

                    from asgiref.sync import sync_to_async
                    # Step 4: Summarize results conversationally
                    chat_response = await sync_to_async(function_response_to_chat)(self.username, self.room_id, result)

                    
                    # json_data = json.loads(f"{result}")
                    # task_workflow_id = json_data["task_workflow_id"]

                    # if "task_workflow_id" in json_data:
                    #     await self.save_msg_with_workflow(
                    #         self.room_id,
                    #         chat_response,
                    #         "AI_Assistant",
                    #         task_workflow_id=task_workflow_id,
                    #     )
                    # else:
                    await self.save_msg(self.room_id, chat_response, "AI_Assistant")

                    # Run process_response asynchronously
                    loop.run_in_executor(None, self.process_final_response, chat_response)

                elif intent == "chat":
                    chat_response = generate_chat_response(prompt)
                    await self.save_msg(self.room_id, prompt, "samuelobinnachimdi")
                    await self.save_msg(self.room_id, chat_response, 'AI_Assistant')
                    
                    # Run process_response asynchronously
                    loop.run_in_executor(None, self.process_final_response, chat_response)

        elif text_data:
            # Handle text messages
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            message_type = text_data_json['message_type']
            sender = text_data_json['sender']

            # Classify intent
            intent = classify_intent(message)

            if intent == 'task':
                # Display the json
                logger.info(f"Intent: {intent}")

                # Step 1: Reassure the user
                assist_response = conversation_assist(message)

                # send to client
                await self.send(text_data=json.dumps({"message": assist_response, "message_type": "text_message", "sender": "AI_Assistant"}))

                # Step 2: Convert prompt to JSON
                json_response = convert_prompt_to_json(message)

                # Display the json
                logger.info(f"JSON Response: {json_response}")

                from asgiref.sync import sync_to_async
                # Step 3: Process JSON and execute tasks
                result = await sync_to_async(process_json_response)("samuelobinnachimdi", self.room_id, json_response)

                # Display the json
                logger.info(f"Result: {result}")

                from asgiref.sync import sync_to_async
                # Step 4: Summarize results conversationally
                chat_response = await sync_to_async(function_response_to_chat)("samuelobinnachimdi", self.room_id, result)

                # send to client
                await self.send(text_data=json.dumps({"message": chat_response, "message_type": "text_message", "sender": "AI_Assistant"}))

                await self.save_msg(self.room_id, message, "samuelobinnachimdi")
                await self.save_msg(self.room_id, chat_response, 'AI_Assistant')
            
            elif intent == "chat":
                # Display the json
                logger.info(f"Intent: {intent}")

                chat_response = generate_chat_response(message)

                # send to client
                await self.send(text_data=json.dumps({"message": chat_response, "message_type": "text_message", "sender": "AI_Assistant"}))
                await self.save_msg(self.room_id, message, "samuelobinnachimdi")
                await self.save_msg(self.room_id, chat_response, 'AI_Assistant')


        # Send back any queued audio responses to the client
        try:
            while True:
                audio_chunk = self.audio_queue.get_nowait()
                await self.send(bytes_data=audio_chunk)
        except queue.Empty:
            pass

    def process_response(self, transcription, response):
        """
        Process the transcription by generating an AI response, converting it to audio,
        and queuing the audio to be sent over the websocket.
        """
        # response = generate_ai_response(transcription)
        response = response
        logger.info(f"Transcription: {transcription}")
        logger.info(f"AI Response: {response}")
        if not response.startswith("AI error"):
            # Convert the AI response text to speech using the text_to_speech utility
            audio = text_to_speech(response, lang='en', tld='co.uk')
            self.audio_queue.put(audio)
        else:
            logger.error(response)
        # Reset the flag after processing is complete
        self.processing_response = False


    def process_final_response(self, response):
        """
        Process the transcription by generating an AI response, converting it to audio,
        and queuing the audio to be sent over the websocket.
        """
        response = response
        logger.info(f"AI Response: {response}")
        if not response.startswith("AI error"):
            # Convert the AI response text to speech using the text_to_speech utility
            audio = text_to_speech(response, lang='en', tld='co.uk')
            self.audio_queue.put(audio)
        else:
            logger.error(response)
        # Reset the flag after processing is complete
        self.processing_response = False



    @sync_to_async
    def save_msg_and_img(self, room_id, text, attatchment, sender_username):
        sender = User.objects.get(username=sender_username)
        chatroom = ChatRoom.objects.get(room_id=room_id)
        chat = Chat.objects.create(room=chatroom, text=text, media_is_img = True, sender=sender)
        chat_media = ChatMedia.objects.create(media=attatchment, chat_id=chat, media_is_img = True)
        chat.media.add(chat_media)
        chat.save()
        return chat
    
    @sync_to_async
    def save_msg_and_vid(self, room_id, text, attatchment, sender_username):
        sender = User.objects.get(username=sender_username)
        chatroom = ChatRoom.objects.get(room_id=room_id)
        chat = Chat.objects.create(room=chatroom, text=text, media_is_vid = True, sender=sender)
        chat_media = ChatMedia.objects.create(media=attatchment, chat_id=chat, media_is_vid = True)
        chat.media.add(chat_media)
        chat.save()
        return chat
    
    @sync_to_async
    def save_msg_and_aud(self, room_id, text, attatchment, sender_username):
        sender = User.objects.get(username=sender_username)
        chatroom = ChatRoom.objects.get(room_id=room_id)
        chat = Chat.objects.create(room=chatroom, text=text, media_is_aud = True, sender=sender)
        chat_media = ChatMedia.objects.create(media=attatchment, chat_id=chat, media_is_aud = True)
        chat.media.add(chat_media)
        chat.save()
        return chat

    @sync_to_async
    def save_msg_and_doc(self, room_id, text, attatchment, sender_username):
        sender = User.objects.get(username=sender_username)
        chatroom = ChatRoom.objects.get(room_id=room_id)
        chat = Chat.objects.create(room=chatroom, text=text, media_is_doc = True, sender=sender)
        chat_media = ChatMedia.objects.create(media=attatchment, chat_id=chat, media_is_doc = True)
        chat.media.add(chat_media)
        chat.save()
        return chat

    @sync_to_async
    def save_msg(self, room_id, text, sender_username):
        sender = User.objects.get(username=sender_username)
        chatroom = ChatRoom.objects.get(room_id=room_id)
        chat = Chat.objects.create(room=chatroom, text=text, sender=sender)
        return chat

    @sync_to_async
    def save_msg_with_workflow(self, room_id, text, sender_username, task_workflow_id):
        sender = User.objects.get(username=sender_username)
        chatroom = ChatRoom.objects.get(room_id=room_id)
        task_workflow = TaskWorkflow.objects.get(id=task_workflow_id) if task_workflow_id else None
        chat = Chat.objects.create(
            room=chatroom,
            text=text,
            sender=sender,
            task_workflow=task_workflow
        )
        return chat
