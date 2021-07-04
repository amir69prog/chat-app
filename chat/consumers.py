import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import FriendList, FriendRequest, MessagePublic, ChatRoomPublic
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
    def messages_to_json(self,messages):
        qss = serialize('json',messages,fields=('content'))
        return qss


    def fetch_messaeges(self,message):
        room = ChatRoomPublic.objects.get(name=self.room)
        messages = MessagePublic.objects.filter(room=room).order_by('timestmap')
        content = {
            'type':'chat_messages',
            'messages':self.messages_to_json(messages),
        }
        self.send_message(content)

    def create_message(self,message):
        ''' Create a new message and send to chat '''
        room = ChatRoomPublic.objects.get(name=self.room)
        new_message = MessagePublic.objects.create(
            author=self.author,
            content=message,
            room=room
        )
        obj_message = MessagePublic.objects.filter(pk=new_message.pk)
        
        content = {
            'type':'chat_messages',
            'messages':self.messages_to_json(obj_message),
        }
        self.send_message(content)
    
    commands = {
        'send':create_message,
        'fetch':fetch_messaeges
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

    def chat_messages(self,content):
        self.send(text_data=json.dumps(content))