from django.urls import path
from chat import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<room_name>/',views.room_public,name='room'),
    path('account/profile/',views.profile_view,name='profile'),
    path('users',views.search,name='search'),
    path('friends',views.friends_list,name='friends'),
    path('request/all',views.friend_requests,name='friend_request'),
    path('user/<username>',views.user_profile,name='user'),
    path('friends/<username>',views.user_friends,name='user_friends'),
    path('chat/<username>',views.chat_private,name='chat_private'),
    path('room/create/',views.create_public_room,name='public_room'),
]
