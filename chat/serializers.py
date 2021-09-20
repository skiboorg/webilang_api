from rest_framework import exceptions, serializers
from djoser.conf import settings
from .models import *
from user.models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'label',
            'image',
        ]

class UserSerializer(serializers.ModelSerializer):
    user_avatar = serializers.CharField(source='get_avatar')
    class Meta:
        model = User
        fields = [
            'id',
            'firstname',
            'firstname_slug',
            'lastname',
            'user_avatar',
            'lastname_slug',
            'is_online',
            'is_superuser'
        ]




class ChatSerializer(serializers.ModelSerializer):
    starter = UserSerializer(many=False, required=False, read_only=True)
    opponent = UserSerializer(many=False, required=False, read_only=True)
    group = GroupSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = Chat
        fields = [
            'id',
            'isNewMessages',
            'updatedAt',
            'starter',
            'opponent',
            'group'

            ]

class ChatsSerializer(serializers.ModelSerializer):
    starter = UserSerializer(many=False,required=False,read_only=True)
    opponent = UserSerializer(many=False,required=False,read_only=True)
    last_message = serializers.CharField(source='get_last_message_text')
    last_message_user_id = serializers.CharField(source='get_last_message_user_id')
    # last_message_user_name = serializers.CharField(source='get_last_message_user_name')
    # last_message_user_status = serializers.BooleanField(source='get_last_message_user_status')
    # last_message_user_avatar = serializers.CharField(source='get_last_message_user_avatar')
    chat_opened = serializers.BooleanField(default=False)
    group = GroupSerializer(many=False,required=False,read_only=True)
    class Meta:
        model = Chat
        fields = [
            'id',
            'isNewMessages',
            # 'updatedAt',
            'starter',
            'opponent',
            'group',
            'chat_opened',

            'last_message',
            'last_message_user_id',
            # 'last_message_user_avatar',
            # 'last_message_user_name',
            # 'last_message_user_status'

                  ]




class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'user',
            'message',
            'file',
            'createdAt',
            ]

class MessagesSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Message
        fields = [
            'id',
            'user',
            'message',
            'isUnread',
            'file',
            'createdAt',
            'chat'
                  ]


