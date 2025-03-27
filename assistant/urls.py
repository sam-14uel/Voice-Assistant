from django.urls import path, include

from webscrape.views import ScrapedDataViewSet, ScrapingTaskViewSet, quick_scrape
from . import views
from authentication import auth
from rest_framework.routers import DefaultRouter
from payments.subscription.utils import subscription_details, subscribe, cancel_subscription, update_subscription

router = DefaultRouter()

router.register("scraping-tasks", ScrapingTaskViewSet)
router.register("scraped-data", ScrapedDataViewSet)

urlpatterns = [
    # Authentication
    path('auth/signup/', auth.SignUpView.as_view(), name='signup'),
    path('auth/signin/', auth.SignInView.as_view(), name='signin'),
    
    path('', include(router.urls)),


    path("quick-scrape/", quick_scrape, name="quick-scrape"),

    path("chat/", views.chat, name="chat"),

    path('chats/c/<room_id>/', views.chat_view, name='chatroom'),
    path('chats/u/@<username>', views.get_or_create_chatroom, name='chat-user'),
    path('chats/', views.my_chatrooms, name='chats'),  
    path('chats/r/<room_id>/edit', views.chatroom_edit_view, name='edit-chatroom'),      
    path('chats/c/<room_id>/leave', views.chatroom_leave_view, name='leave-chatroom'), # type: ignore
    path('chats/r/<room_id>/delete', views.chatroom_delete_view, name='delete-chatroom'),
    path('chats/r/<room_id>/', views.chatroom_delete_view, name='request-join-room'),
    path('chat/<chat_id>/delete', views.delete_chat, name='delete-chat'),
    path('chats/r/create_group_chat', views.create_groupchat, name='create-groupchat'), # type: ignore


    # Payments
    path('subscription/details/', subscription_details, name='subscription_details'),
    path('subscription/update/', update_subscription, name='update_subscription'),
    path('subscription/cancel/', cancel_subscription, name='cancel_subscription'),
    path('subscribe/', subscribe, name='subscribe'),
]