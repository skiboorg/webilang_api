import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope["path"])
        # print(self.scope['url_route']['kwargs']['chat_id'])
        self.room_name = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.room_name)
        # print(self.room_group_name)
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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))

    # Receive message from room group
    async def chat_gift(self, event):
        gift_img = event['gift_img']
        gift_price = event['gift_price']
        gift_message = event['gift_message']
        gift_from = event['gift_from']
        gift_to = event['gift_to']
        gift_from_avatar = event['gift_from_avatar']
        gift_from_fio = event['gift_from_fio']
        gift_time = event['gift_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type':'gift',
            'gift_img': gift_img,
            'gift_price': gift_price,
            'gift_message': gift_message,
            'gift_from': gift_from,
            'gift_to': gift_to,
            'gift_from_avatar': gift_from_avatar,
            'gift_from_fio': gift_from_fio,
            'gift_time': gift_time,
        }))
