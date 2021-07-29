from chat.consumers import ChatConsumer,RequestConsumer,FriendConsumer,ChatPrivateConsumer
from django.urls import re_path


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/?$',ChatConsumer.as_asgi()),
    re_path('request/',RequestConsumer.as_asgi()),
    re_path('friends/',FriendConsumer.as_asgi()),
    re_path(r'private/chat/(?P<username>\w+)/?$',ChatPrivateConsumer.as_asgi()),
]