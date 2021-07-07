from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Thread, Message
from trade.models import User
import json
from channels.db import database_sync_to_async

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
            me = self.scope['url_route']['kwargs']['user']
            print(me)
            me = await sync_to_async(User.objects.get)(id=me)
            other_username = self.scope['url_route']['kwargs']['username']
            print(other_username)
            other_user = await sync_to_async(User.objects.get)(id=other_username)
            # print(other_user)
            self.thread_obj = await sync_to_async(Thread.objects.get_or_create_personal_thread)(me, other_user)
            # print(self.thread_obj)
            self.room_name = "chat-%s" % self.thread_obj.id
            # print(self.room_name)
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.send({
                'type': 'websocket.accept',

            })

            print(f'[{self.channel_name}] - you are connected')


    async def websocket_receive(self, event):
        my_list=[]
        your_list=[]
        me = self.scope['url_route']['kwargs']['user']
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        data = Message.objects.filter(thread=self.thread_obj).values('text', "time", 'sender')

        for i in data:
            # print(i)
            my_list.append(i)
            # print(my_list)

        msg = json.dumps(
            {
                'type': event.get('text'),
                'text': str(User.objects.get(id=me)),
                "command":str(my_list)
            }
        )
        print(msg)
        print(event.get('text'))
        await self.store_message(event.get('text'))

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'websocket.message',
                'text': msg,
                # 'command': my_list

            }
        )
        print(self.room_name)

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - message sent - {event["text"]}')
        await self.send({
            'type': 'websocket.send',
            'text': event["text"],
        }
        )

    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disconnected')
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    @database_sync_to_async
    def store_message(self, text):
        me = self.scope['url_route']['kwargs']['user']
        Message.objects.create(
            thread=self.thread_obj,
            sender=User.objects.get(id=me),
            text=text
        )
