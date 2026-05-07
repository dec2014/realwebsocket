import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .templatetags.chatextras import initials
from django.utils.timesince import timesince
from .models import Room,Messages
from account.models import User
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_name_group=f'chat_{self.room_name}'
        await asyncio.sleep(0.1)
        await self.get_room()
        await self.channel_layer.group_add(self.room_name_group,self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name_group,self.channel_name)

    async def receive(self, text_data = None, bytes_data = None):

        text_data_json=json.loads(text_data)
        type=text_data_json['type']
        message=text_data_json['message']
        name=text_data_json['name']
        agent=text_data_json.get('agent','')

        print('type',type)

        if type=='message':
            nw_message= await self.create_messages(name,agent,message)
            # print(nw_message)
            await self.channel_layer.group_send(
                self.room_name_group,{
                    'type':'chat_message',
                    'message':message,
                    'name':name,
                    'agent':agent,
                    'initials':initials(name),
                    'created_at':timesince(nw_message.created_at)

                }
            )
    async def chat_message(self,event):
        await self.send(text_data=json.dumps(event))
        


    @sync_to_async
    def get_room(self):
        self.room=Room.objects.get(uuid=self.room_name)   

    @sync_to_async
    def create_messages(self,sent_by,agent,message):
        message=Messages.objects.create(body=message,sent_by=sent_by)
        if agent:
            message.created_by=User.objects.get(pk=agent)
            message.save()
        self.room.messages.add(message)
        return message