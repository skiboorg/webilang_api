from rest_framework import serializers
from .models import *
from user.models import User
from lesson.models import *
from group.models import *

class FileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = '__all__'

    def get_filename(self, obj):
        print(obj)
        try:
            return obj.url
        except:
            print('fileserializer error')


class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Folder
        fields = '__all__'


class UploadedHomeWorkFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedHomeWorkFile
        fields = '__all__'


class UploadedMaterialFileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = UploadedMaterialFile
        fields = '__all__'

    def get_filename(self, obj):
        return obj.file.url.split('/')[4]

class GroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'firstname',
            'firstname_slug',
            'lastname',
            'lastname_slug',
            'is_present',
            'selected_reward'
        ]

class GroupSerializer(serializers.ModelSerializer):
    users = GroupUserSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Group
        fields = '__all__'

class LessonPresenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPresence
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False, required=False, read_only=True)
    homeWork = FileSerializer(many=True, required=False, read_only=True)
    material = FileSerializer(many=True, required=False, read_only=True)
    uploaded_homework = UploadedHomeWorkFileSerializer(many=True, required=False, read_only=True)
    uploaded_material = UploadedMaterialFileSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'







