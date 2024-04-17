import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main import models
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        # 올바른 채널 이름을 사용하여 그룹에서 제거
        await self.channel_layer.group_discard(
            self.roomGroupName,  # 그룹 이름
            self.channel_name       # 채널 이름
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        message_obj = await self.store_message(username, message)
        timestamp = message_obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "message" : message , 
                "username" : username ,
                 "timestamp": timestamp
            })
        await self.store_message(username, message)

    async def sendMessage(self , event) : 
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"]
        }))

    @database_sync_to_async
    def store_message(self, username, message):
        # Message 모델에 메시지 저장
        return models.Message.objects.create(username=username, message=message)
      
