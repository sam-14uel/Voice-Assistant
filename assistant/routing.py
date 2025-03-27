from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/conversation/<room_id>/", consumers.ConversationConsumer.as_asgi()),
]