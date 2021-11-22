import json
from functools import reduce
import requests

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from .serializers import *
# from notification.services import createNotification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from notification.models import Notification
from user.models import UserNotification

channel_layer = get_channel_layer()

class GetSpecificChat(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    def get_object(self):
        try:
            opponent_id = self.request.query_params.get('o_id')
            print(opponent_id)
            starter = self.request.user
            opponent = User.objects.get(id=opponent_id)
            chat = None
            try:
                chat = Chat.objects.get(starter=starter,opponent=opponent)
                print('chat starter opponent found')
            except:
                print('chat starter opponent not found')
            if not chat:
                try:
                    chat = Chat.objects.get(starter=opponent, opponent=starter)
                    print('chat opponent starter found')
                except:
                    print('chat opponent starter not found')

            if not chat:
                chat = Chat.objects.create(starter=starter, opponent=opponent)
                chat.users.add(starter)
                chat.users.add(opponent)
                print('chat created')


            # chat,created = Chat.objects.get_or_create(starter=starter,opponent=opponent)
            # if created:
            #     chat.users.add(self.request.user)
            #     chat.users.add(opponent)
            #     print('chat created')
            return chat
        except:
            return 0




class GetChat(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    def get_object(self):
        chat_id = self.request.query_params.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        return chat



class MessagesList(generics.ListAPIView):
    """Вывод сообщений в чате"""
    serializer_class = MessagesSerializer
    def get_queryset(self):
        chat_id=self.request.query_params.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        messages = Message.objects.filter(chat=chat)

        # unread_notifications = Notification.objects.filter(type='chat',user=self.request.user,chat_id=chat_id)
        # unread_notifications.update(is_new=False)

        return messages

    # def get(self,request, chat_id):
    #     chat = Chat.objects.get(id=chat_id)
    #     messages = Message.objects.filter(chat=chat)
    #     serializer = MessagesSerializer(messages, many=True)
    #     return Response(serializer.data)

class ChatsList(generics.ListAPIView):
    """Вывод чатов"""
    serializer_class = ChatsSerializer
    def get_queryset(self):
        chats = Chat.objects.filter(users__in=[self.request.user.id]).order_by('-updatedAt')
        print(chats)
        return chats

class SetChatRead(APIView):
    def post(self,request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        messages = chat.messages
        chat.isNewMessages = False
        chat.save()
        messages.update(isUnread=False)
        # notify = Notification.objects.filter(user=request.user, chat_id=chat_id)
        # notify.delete()
        return Response(status=200)


class ChatAdd(APIView):

    """Добавить сообщение в чат"""
    def post(self,request, chat_id):
        print(request.data)
        message = json.loads(request.data['message'])



        chat = Chat.objects.get(id=chat_id)
        new_message = Message.objects.create(chat=chat,
                                             user=request.user,
                                             message=message,
                                             )

        for f in request.FILES.getlist('file'):
            new_message.file = f
            new_message.save(update_fields=['file'])

        message = MessageSerializer(new_message,many=False)
        async_to_sync(channel_layer.group_send)('chat_%s' % chat.id,
                                                {"type": "chat.message", 'message': message.data, 'chatId': chat_id})
        for user in chat.users.all():
            if user != request.user:
                if user.channel:
                    # createNotification('chat', user, 'Новое сообщение в чате', '/lk/chats', chat_id=chat.id)
                    UserNotification.objects.create(user=user, is_chat=True)
                    async_to_sync(channel_layer.send)(user.channel,
                                                      {
                                                          "type": "user.notify",
                                                          'message': 'Новое сообщенеи в чате',
                                                          'event': 'new_chat_mgs',
                                                          'chatId': chat_id
                                                      })
        return Response(status=201)


class ChatNewMessage(APIView):
    """Добавить сообщение в чат"""
    def post(self,request):
        data = request.data
        chat_opponent = User.objects.get(nickname=data['o_id'])
        c = [request.user.id, chat_opponent.id]
        chats = Chat.objects.annotate(cnt=models.Count('users')).filter(cnt=len(c),group__is_null=True) #ADDED  ,is_stream_chat=False
        chat_qs = reduce(lambda qs, pk: qs.filter(users=pk), c, chats)

        if len(chat_qs) == 0:
            chat = Chat.objects.create(starter=request.user, opponent=chat_opponent)
            chat.users.add(request.user)
            chat.users.add(chat_opponent)
        else:
            chat = chat_qs[0]

        # print(request.data)

        # print(msg_to)
        # createNotification('chat', chat_opponent, 'Новое сообщение в чате', '/lk/chats',chat_id=chat.id)
        # async_to_sync(channel_layer.send)(chat_opponent.channel, {"type": "user.notify"})

        Message.objects.create(chat=chat,
                               user=request.user,
                               message=data['message'])

        return Response(status=200)

