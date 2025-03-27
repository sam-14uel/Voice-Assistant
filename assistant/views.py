from django.shortcuts import render

# Create your views here.


def chat(request):
    return render(request, 'index.html')




from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse
#from social_network.other_models.media import ChatMedia
from ai_agent.models import ChatRoom, Chat, ChatMedia
from django.contrib.auth.models import User

@login_required
def chat_view(request, room_id):
    chat_group = get_object_or_404(ChatRoom, room_id=room_id)
    chat_messages = Chat.objects.filter(room=chat_group).order_by('created')
    #chat_messages = Chat.objects.filter(room=chat_group).prefetch_related('chat_media')

    current_user = request.user  # Get the logged-in user

    # Subquery to get the latest chat date for each chat room
    latest_chat_date = Chat.objects.filter(room=OuterRef('pk')).order_by('-created').values('created')[:1]

    # Annotate ChatRoom with the latest chat date and filter by membership, then order by the latest chat date
    chatrooms = ChatRoom.objects.filter(members=current_user).annotate(
        latest_chat_date=Subquery(latest_chat_date, output_field=DateTimeField())
    ).order_by('-latest_chat_date', '-created')

    chatroom_data = []
    for chatroom in chatrooms:
        if chatroom.is_private:
            other_member =  chatroom.members.exclude(username=request.user.username)
            for member in other_member:
                # room_pic = member.profile.profile_picture.url
                room_name = f"{member.first_name} " + f"{member.last_name}"
                room_u_name = member.username
                # verified = member.profile.verified
                #online_status = OnlineStatus.objects.get(user=member)
                room_is_private = chatroom.is_private
        else:
            # room_pic = chatroom.group_picture.url
            room_name = chatroom.group_name
            room_u_name = ''
            # verified = False
            #online_status = None,
            room_is_private = chatroom.is_private

        chatroom_data.append({
            'room_name': room_name,
            # 'room_pic': room_pic,
            'room_id': chatroom.room_id,
            'room_u_name': room_u_name,
            # 'verified': verified,
            'room_is_private': room_is_private,
            #'online_status': online_status,
        })

    
    other_user = chat_group.members.exclude(username=request.user.username)

    # for user in other_user:
        #online_status = OnlineStatus.objects.get(user=user)

    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            return redirect('chats')
        else:
            context = {
                'chat_messages' : chat_messages,
                'other_user' : other_user,
                'chatroom_data': chatroom_data,
                'chat_group' : chat_group,
                'chatrooms': chatrooms,
                #'online_status': online_status,
            }
            return render(request, 'chat/index.html', context)
            
    elif chat_group.is_private == False:
        if request.user not in chat_group.members.all():
            return redirect('join-group-request', chat_group.room_id)
        elif request.user in chat_group.members.all():
            context = {
                'chat_messages' : chat_messages,
                'chat_group' : chat_group,
                'chatrooms': chatrooms,
                'chatroom_data': chatroom_data,
            }
            return render(request, 'chats/group_chats.html', context)
    
    
    
    context = {
        'chat_messages' : chat_messages,
        'other_user' : other_user,
        'chat_group' : chat_group,
        #'chatrooms': chatrooms,
    }
    
    return render(request, 'a_rtchat/chat.html', context)



from django.db import transaction
from django.shortcuts import get_object_or_404

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    # Ensure the other user exists
    other_user = get_object_or_404(User, username=username)

    # Efficiently find an existing private chatroom where both users are members
    chatroom = ChatRoom.objects.filter(
        is_private=True,
        members=request.user
    ).filter(
        members=other_user
    ).distinct().first()

    if not chatroom:
        # Use a transaction to create a new chatroom if none exists
        with transaction.atomic():
            chatroom = ChatRoom.objects.create(admin=request.user, is_private=True)
            chatroom.members.add(request.user, other_user)

    return redirect('chatroom', chatroom.room_id)


#@login_required
def create_groupchat(request):
    
    if request.method == 'POST':
        group_name = request.POST['group_name']
        new_group_chat = ChatRoom.objects.create(admin=request.user, group_name=group_name)
        new_group_chat.members.add(request.user)
        new_group_chat.save()
        return redirect('chatroom', new_group_chat.room_id)


@login_required
def chatroom_edit_view(request, room_id):
    chat_group = get_object_or_404(ChatRoom, room_id=room_id)
    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == 'POST':
        new_group_name = request.POST['group_name']
        group_chat = ChatRoom.objects.update(room_id=room_id, group_name=new_group_name)
        remove_members = request.POST.getlist('remove_members')
        for member_id in remove_members:
            member = User.objects.get(id=member_id)
            chat_group.members.remove(member)  
            
        return redirect('chatroom', chat_group.room_id)
    
    context = {
        'chat_group' : chat_group
    }   
    return render(request, 'a_rtchat/chatroom_edit.html', context) 


@login_required
def chatroom_delete_view(request, room_id):
    chat_group = get_object_or_404(ChatRoom, room_id=room_id)
    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == "POST":
        chat_group.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('home')
    
    return render(request, 'a_rtchat/chatroom_delete.html', {'chat_group':chat_group})


#@login_required
def chatroom_leave_view(request, room_id):
    chat_group = get_object_or_404(ChatRoom, room_id=room_id)
    if request.user not in chat_group.members.all():
        raise Http404()
    
    if request.method == "POST":
        chat_group.members.remove(request.user)
        messages.success(request, 'You left the Chat')
        return redirect('home')




from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, DateTimeField

@login_required
def my_chatrooms(request):
    current_user = request.user  # Get the logged-in user

    # Subquery to get the latest chat date for each chat room
    latest_chat_date = Chat.objects.filter(room=OuterRef('pk')).order_by('-created').values('created')[:1]

    # Annotate ChatRoom with the latest chat date and filter by membership, then order by the latest chat date
    chatrooms = ChatRoom.objects.filter(members=current_user).annotate(
        latest_chat_date=Subquery(latest_chat_date, output_field=DateTimeField())
    ).order_by('-latest_chat_date', '-created')

    #Determine image to display
    chatroom_data = []
    for chatroom in chatrooms:
        if chatroom.is_private:
            other_member =  chatroom.members.exclude(username=request.user.username)
            for member in other_member:
                room_pic = member.profile.profile_picture.url
                room_name = f"{member.first_name} " + f"{member.last_name}"
                room_u_name = member.username
                verified = member.profile.verified
                #online_status = OnlineStatus.objects.get(user=member)
                room_is_private = chatroom.is_private
        else:
            room_pic = chatroom.group_picture.url
            room_name = chatroom.group_name
            room_u_name = ''
            verified = False
            #online_status = None,
            room_is_private = chatroom.is_private

        chatroom_data.append({
            'room_name': room_name,
            'room_pic': room_pic,
            'room_id': chatroom.room_id,
            'room_u_name': room_u_name,
            'verified': verified,
            'room_is_private': room_is_private,
            #'online_status': online_status,
        })

    if chatrooms:
        context = {
            'chatrooms': chatrooms,
            #'other_member': other_member,
            'chatroom_data': chatroom_data
            }
        return render(request, 'chats/chats.html', context)
    else:
        return render(request, 'chats/chats.html')


def delete_chat(request, chat_id):
    chat = Chat.objects.get(chat_id=chat_id)
    chat_medias = ChatMedia.objects.filter(chat_id=chat)
    if request.user == chat.sender:
        chat.delete()
        if chat_medias:
            chat_medias.delete()
            return JsonResponse({
                'message': f'successfully deleted chat {chat.chat_id} with {chat_medias.count()} media files',
                'status': 'successfull',
            }, safe=True)
        return JsonResponse({
            'message': f'successfully deleted chat {chat.chat_id}',
            'status': 'successfull',
        }, safe=True)
    elif request.user != chat.sender:
        return JsonResponse({
            'message': f'cannot delete chat {chat.chat_id}',
            'status': 'permission_denied',
        }, safe=True)
    else:
        return JsonResponse({
            'message': f'error occured while deleting chat {chat.chat_id}',
            'status': 'no_action',
        }, safe=True)
