import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.db.models import fields 
from .models import Message, Room
from django.core.serializers import serialize

class ChatConsumer(WebsocketConsumer):
    def messages_to_json(self,messages):
        qss = serialize('json',messages,fields=('content'))
        return qss


    def fetch_messaeges(self,message):
        room = Room.objects.get(name=self.room)
        messages = Message.objects.filter(room=room).order_by('timestmap')
        content = {
            'type':'chat_messages',
            'messages':self.messages_to_json(messages),
        }
        self.send_message(content)

    def create_message(self,message):
        ''' Create a new message and send to chat '''
        room = Room.objects.get(name=self.room)
        new_message = Message.objects.create(
            author=self.author,
            content=message,
            room=room
        )
        obj_message = Message.objects.filter(pk=new_message.pk)
        
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