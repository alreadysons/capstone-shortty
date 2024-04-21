import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import Message, Category
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "group_chat"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def send_message(self, event):
        # 클라이언트에게 WebSocket 메시지를 보냅니다.
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
            'category': event.get('category', 'No Category')  # 카테고리가 제공되지 않은 경우 기본값
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        category_id = text_data_json.get('categoryId')
        
        # WebSocket 연결을 통해 인증된 사용자의 이름을 가져오거나, 세션에서 익명 ID를 가져옵니다.
        username = (self.scope['user'].username if self.scope['user'].is_authenticated 
                    else self.scope['session'].get('anonymous_id', 'Anonymous'))

        # 메시지가 비어 있거나 카테고리 ID가 제공되지 않았을 경우, 메시지 전송을 중단합니다.
        if not message or not category_id:
            print("Incomplete data received: Message and Category ID are required.")
            return

        category = await self.get_category(category_id)
        if not category:
            print(f"Category with id {category_id} does not exist.")
            return

        message_obj = await self.store_message(username, message, category)
        timestamp = message_obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # 메시지를 그룹에 전송합니다.
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'username': username,
                'category': category.name,
                'timestamp': timestamp
            }
        )
    @database_sync_to_async
    def get_category(self, category_id):
        # Category.DoesNotExist 예외를 처리합니다.
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    @database_sync_to_async
    def store_message(self, username, message, category):
        # category가 None이 아닌 경우에만 Message 객체를 저장합니다.
        if category is not None:
            return Message.objects.create(username=username, message=message, category=category)
        else:
            return Message.objects.create(username=username, message=message)