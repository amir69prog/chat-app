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
]