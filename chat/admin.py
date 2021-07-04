from django.contrib import admin
from .models import (
    MessagePublic,
    ChatRoomPublic,
    Profile,
    FriendList,
    ChatRoomPrivate,
    MessagePrivate,
    FriendRequest,
)

admin.site.register(MessagePublic)
admin.site.register(ChatRoomPublic)
admin.site.register(Profile)
admin.site.register(FriendList)
admin.site.register(ChatRoomPrivate)
admin.site.register(MessagePrivate)
admin.site.register(FriendRequest)