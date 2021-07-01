from channels.consumer import SyncConsumer, AsyncConsumer
from asgiref.sync import async_to_sync, sync_to_async
# from django.contrib.auth.models import User
from .models import Thread, Message
from trade.models import User
import json
from channels.db import database_sync_to_async

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        a = self.scope['headers'][4]
        print(type(a))
        head = a[0]
        auth = head.decode('utf-8')
        print(auth)
        if auth == 'authorization':
            data = a[1]
            print(data.decode("utf-8"))
            username = data.decode("utf-8")
            me = await sync_to_async(User.objects.get)(id=username)
            # print(me)
            other_username = self.scope['url_route']['kwargs']['username']
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
        a = self.scope['headers'][0]
        head = a[0]
        auth = head.decode('utf-8')
        print(auth)
        if auth == 'authorization':
            data = a[1]
            print(data.decode("utf-8"))
            username = data.decode("utf-8")
            me = await sync_to_async(User.objects.get)(id=username)
            # print(me)
            other_username = self.scope['url_route']['kwargs']['username']
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
        print(f'[{self.channel_name}] - Received message - {event["text"]}')
        a = self.scope['headers'][0]
        head = a[0]
        auth = head.decode('utf-8')
        print(auth)
        if auth == 'authorization':
            data = a[1]
            print(data.decode("utf-8"))
            username = data.decode("utf-8")
            msg = json.dumps(
                {
                    'type': event.get('text'),
                    'text': str(User.objects.get(id=username)), }
            )

        a = self.scope['headers'][4]
        head = a[0]
        auth = head.decode('utf-8')
        print(auth)
        if auth == 'authorization':
            data = a[1]
            print(data.decode("utf-8"))
            username = data.decode("utf-8")
            msg = json.dumps(
                {
                    'type': event.get('text'),
                    'text': str(User.objects.get(id=username)), }
            )
        print(msg)

        await self.store_message(event.get('text'))

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'websocket.message',
                'text': msg,
            }
        )
        print(self.room_name)

    async def websocket_message(self, event):
        print(f'[{self.channel_name}] - message sent - {event["text"]}')
        await self.send({
            'type': 'websocket.send',
            'text': event.get('text'),
        }
        )

    async def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disconnected')
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    @database_sync_to_async
    def store_message(self, text):
        a = self.scope['headers'][4]
        head = a[0]
        auth = head.decode('utf-8')
        print(auth)
        if auth == 'authorization':
            data = a[1]
            print(data.decode("utf-8"))
            username = data.decode("utf-8")
            Message.objects.create(
                thread=self.thread_obj,
                sender=User.objects.get(id=username),
                text=text
            )
        a = self.scope['headers'][0]
        print(type(a))
        head = a[0]
        auth = head.decode('utf-8')
        print(auth)
        if auth == 'authorization':
            data = a[1]
            print(data.decode("utf-8"))
            username = data.decode("utf-8")
            Message.objects.create(
                thread=self.thread_obj,
                sender=User.objects.get(id=username),
                text=text
            )