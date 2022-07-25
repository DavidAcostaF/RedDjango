import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from apps.usuarios.models import ChatMessage, Thread, Usuario

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.usuario = self.scope['url_route']['kwargs']['usuario']
#         self.room_group_name = 'chat_%s' % self.usuario

#         await self.channel_layer

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('connected',event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,event):
        print('receive',event)
        receive_data = json.loads(event['text'])
        msg = receive_data.get('message')
        sent_by_id = receive_data.get('sent_by')
        send_to_id = receive_data.get('send_to')
        thread_id = receive_data.get('thread_id')
        if not msg:
            print('Error:: empty message')
            return False

        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)

        if not sent_by_user:
            print('Error:: sent by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not thread_obj:
            print('Error:: Thread is incorrect')

        await self.create_chat_message(thread_obj,sent_by_user,msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self.user = self.scope['user']

        response = {
            'message':msg,
            'sent_by':self.user.id,
            'thread_id':thread_id
        }
        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text':json.dumps(response)
            }
        )
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text':json.dumps(response)
            }
        )
        
        print(response)

    async def websocket_disconnect(self,event):
        print('disconnected',event)
    
    async def chat_message(self,event):
        print('chat_mesage',event)
        await self.send(
            {
                'type': 'websocket.send',
                'text': event['text']
                }
        )

    @database_sync_to_async
    def get_user_object(self,user_id):
        qs = Usuario.objects.filter(id = user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self,thread_id):
        qs = Thread.objects.filter(id = thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj
    
    @database_sync_to_async
    def create_chat_message(self,thread,user,msg):
        ChatMessage.objects.create(thread = thread,user= user,message =msg)