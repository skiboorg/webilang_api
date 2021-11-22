from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser import utils
from rest_framework import exceptions, serializers, status, generics
from .models import *
from djoser.conf import settings
from lesson.models import File,Folder
from rest_framework.response import Response

# User = get_user_model()



class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class UserRewardSerializer(serializers.ModelSerializer):
    reward = RewardSerializer(many=False,required=False,read_only=True)
    class Meta:
        model = UserReward
        fields = '__all__'


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = '__all__'

    def get_filename(self, obj):

        return obj.file.url.split('/')[4]


class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Folder
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_avatar = serializers.SerializerMethodField()
    rewards = UserRewardSerializer(many=True,required=False,read_only=True)
    files = FileSerializer(many=True,required=False,read_only=True)
    folders = FolderSerializer(many=True,required=False,read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'user_avatar',
            'firstname',
            'firstname_slug',
            'lastname',
            'lastname_slug',
            'about',
            'email',
            'country',
            'phone',
            'city',
            'birthday',
            'total_progress',
            'personal_lessons_left',
            'group_lessons_left',
            'is_online',
            'last_online',
            'promo',
            'is_time_24h',
            'is_teacher',
            'rewards',
            'files',
            'folders',

        ]


    def get_user_avatar(self, obj):
        if obj.chosen_avatar:
            return self.context['request'].build_absolute_uri(obj.chosen_avatar.image.url)
        elif obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url)
        elif obj.social_avatar:
            return obj.social_avatar
        else:
            return '/no-avatar.svg'

# djoser/utils.py проыерка на регу соц сетей

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'email',
            'firstname',
            'lastname',
            "password",
            'social_avatar',
            'is_social_register',
            # settings.LOGIN_FIELD,
            User._meta.pk.name,

        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        print(validated_data)
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        print('validated_data',validated_data)
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user




