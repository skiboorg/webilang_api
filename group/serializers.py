from rest_framework import serializers
from .models import *
from user.models import User
from lesson.models import *


# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = '__all__'

    def get_filename(self, obj):

        return obj.file.url.split('/')[4]

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class UploadedHomeWorkFileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = UploadedHomeWorkFile
        fields = '__all__'
    def get_filename(self, obj):
        return obj.file.url.split('/')[5]

class UploadedMaterialFileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = UploadedMaterialFile
        fields = '__all__'

    def get_filename(self, obj):
        return obj.file.url.split('/')[5]



class LessonSerializer(serializers.ModelSerializer):
    homeWork = FileSerializer(many=True, required=False, read_only=True)
    material = FileSerializer(many=True, required=False, read_only=True)
    uploaded_homework = UploadedHomeWorkFileSerializer(many=True, required=False, read_only=True)
    uploaded_material = UploadedMaterialFileSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'


class GroupUserSerializer(serializers.ModelSerializer):
    user_avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            # 'avatar',
            # 'social_avatar',
            # 'chosen_avatar',
            'user_avatar',
            'firstname',
            'firstname_slug',
            'lastname',
            'lastname_slug',
            'about',
            'email',
            'phone'
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


class GroupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupType
        fields = '__all__'


class GroupLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupLevel
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    type = GroupTypeSerializer(many=False, required=False, read_only=True)
    level = GroupLevelSerializer(many=False, required=False, read_only=True)
    teacher = GroupUserSerializer(many=False, required=False, read_only=True)
    users = GroupUserSerializer(many=True, required=False, read_only=True)
    lessons = LessonSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Group
        fields = '__all__'


