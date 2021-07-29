import json
from channels.generic.websocket import WebsocketConsumer,AsyncConsumer
from asgiref.sync import async_to_sync
from .models import FriendList, FriendRequest, MessagePrivate, MessagePublic, ChatRoomPublic,ChatRoomPrivate
from django.core.serializers import serialize
import chat.Internalfunctions as func
from chat.models import User

class RequestConsumer(WebsocketConsumer):

    def cancel_request(self,message):
        receiver_username = message['receiver']
        receiver = User.objects.get(username=receiver_username)
        request = func.cancel_request(receiver,self.user)
        content = {
            'action':'cancel',
            'status':'good'
        }
        if not request:
            content['status'] = 'bad'
        self.send_message(content)


    def decline_request(self,message):
        sender_username = message['sender']
        sender = User.objects.get(username=sender_username)
        request = func.decline_request(self.user,sender)
        content = {
            'action':'decline',
            'status':'good'
        }
        if not request:
            content['status'] = 'bad'
        self.send_message(content)


    def accept_request(self,message):
        sender_username = message['sender']
        sender = User.objects.get(username=sender_username)
        request = func.accept_request(self.user,sender)
        content = {
            'action':'accept',
            'status':'good'
        }
        if not request:
            content['status'] = 'bad'
        self.send_message(content)


    def send_request(self,message):
        receiver_username = message['receiver']
        receiver = User.objects.get(username=receiver_username)
        request = func.create_request(receiver,self.user)
        content = {
            'action':'send',
            'status':'good'
        }
        if not request:
            content['status'] = 'bad'
        self.send_message(content)

    commands = {
        'cancel':cancel_request,
        'decline':decline_request,
        'accept':accept_request,
        'send':send_request,
    }

    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.commands[data['action']](self,data)

    def disconnect(self, code):
        pass

    def send_message(self,content):
        data = json.dumps(content)
        print(data)
        self.send(data)


class FriendConsumer(WebsocketConsumer):

    def remove(self,message):
        friend_username = message['friend']
        friend = User.objects.get(username=friend_username)
        friend_list = FriendList.objects.get(user=self.user)
        friend_list.remove_friend(friend)
        content = {
            'action':'remove',
            'status':'good'
        }
        self.send_messages(content)


    commands = {
        'remove':remove,
    }

    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.commands[data['action']](self,data)

    def disconnect(self, code):
        pass
    
    def send_messages(self,content):
        data = json.dumps(content)
        self.send(data)


class ChatConsumer(WebsocketConsumer):
    def message_to_json(self,message):
        data = {
            'author':message.author.username,
            'content':message.content,
            'profile_picture':message.author.profile.profile_picture.url,
        }
        return data
    
    def create_message(self,message):
        ''' Create a new message and send to chat '''
        room = ChatRoomPublic.objects.get(name=self.room)
        new_message = MessagePublic(
            author=self.author,
            content=message,
            room=room
        )
        new_message.save()
        content = {
            'type':'chat_message',
            'message':self.message_to_json(new_message)
        }
        self.send_message(content)
    
    commands = {
        'send':create_message,
    }


    def connect(self):
        ''' Enter user to this Group '''
        self.room = self.scope['url_route']['kwargs']['room_name']
        self.group = f'chat_room_{self.room}'
        self.author = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            self.group,
            self.channel_name
        )
        self.accept()


    def disconnect(self,code):
        ''' live user from this Group '''
        async_to_sync(self.channel_layer.group_discard)(
            self.group,
            self.channel_name
        )

    def receive(self,text_data):
        data = json.loads(text_data)
        message = data['message']
        self.commands[data['command']](self,message)

    def send_message(self,content):
        async_to_sync(self.channel_layer.group_send)(
            self.group,
            content
        )

    def chat_message(self,content):
        self.send(text_data=json.dumps(content))
        print(content)

class ChatPrivateConsumer(WebsocketConsumer):
    def message_to_json(self,message):
        data = {
            'author':message.author.username,
            'content':message.content,
            'profile_picture':message.author.profile.profile_picture.url,
        }
        return data

    
    def create_message(self,message):
        new_message = MessagePrivate(
            author=self.user,
            content=message,
            room=self.room_name
        )
        new_message.save()
        
        content = {
            'type':'send_data',
            'message':self.message_to_json(new_message),
            'action':'new_message',
        }
        self.send_message(content)
    
    def send_message(self,content):
        async_to_sync(self.channel_layer.group_send)(
            self.group,
            content
        )

    def send_data(self,content):
        self.send(text_data=json.dumps(content))

    commands = {
        'send_message':create_message
    }


    def get_room(self):
        qs = ChatRoomPrivate.get_room(self.user,self.friend)
        return qs

    def connect(self):
        self.user_name = self.scope['user']
        self.friend_name = self.scope['url_route']['kwargs']['username']
        self.user = User.objects.get(username=self.user_name)
        self.friend = User.objects.get(username=self.friend_name)
        self.room_name = self.get_room()
        print(self.room_name)
        self.group = f'chat_private_{str(self.room_name)}'
        async_to_sync(self.channel_layer.group_add)(
            self.group,
            self.channel_name
        )
        print(self.user)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        self.commands[data['type']](self,message)
