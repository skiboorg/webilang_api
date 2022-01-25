import json

from pytils.translit import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from user.models import UserReward,UserNotification, Reward
from django.core.files.base import ContentFile

class GetFolders(generics.ListAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

class GetFiles(generics.ListAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()


class GetLesson(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.filter()


class GetTeacherLessons(generics.ListAPIView):
    serializer_class = LessonSerializer
    def get_queryset(self):
        return Lesson.objects.filter(group__teacher=self.request.user)

# class GetTeacherFolders(generics.ListAPIView):
#     serializer_class = FolderSerializer
#     def get_queryset(self):
#         return Folder.objects.filter(group__teacher=self.request.user)


class GetLessonPresence(generics.ListAPIView):
    serializer_class = LessonPresenceSerializer
    def get_queryset(self):
        return LessonPresence.objects.filter(lesson_id=self.request.query_params.get('l_id'))


class DeleteFolder(APIView):
    def post(self, request):
        Folder.objects.get(id=request.data.get('id')).delete()
        return Response(status=200)


class DeleteFile(APIView):
    def post(self, request):

        fileType  = request.data.get('list')
        if fileType:
            if fileType == 'home_work':
                UploadedHomeWorkFile.objects.get(id=request.data['id']).delete()
            if fileType == 'materials':
                UploadedMaterialFile.objects.get(id=request.data['id']).delete()
        else:
            File.objects.get(id=request.data['id']).delete()
        return Response(status=200)

class SaveLessonFiles(APIView):
    def post(self, request):

        materials = request.data['selectedMaterials']
        homeworks = request.data['selectedHomework']

        selectedMaterials = []
        selectedHomeworks = []
        comment = request.data['comment']
        if materials:
            selectedMaterials = json.loads(materials)
        if homeworks:
            selectedHomeworks = json.loads(homeworks)
        id = json.loads(request.data['id'])
        lesson = Lesson.objects.get(id=id)
        lesson.comment = comment
        lesson.save()
        lesson.homeWork.clear()
        lesson.material.clear()
        for file in selectedHomeworks:
            lesson.homeWork.add(file['id'])
        for file in selectedMaterials:
            lesson.material.add(file['id'])
        for file in request.FILES.getlist('uploaded_homework'):
            UploadedHomeWorkFile.objects.create(
                lesson=lesson,
                file=file)
        for file in request.FILES.getlist('uploaded_materials'):
            UploadedMaterialFile.objects.create(
                lesson=lesson,
                file=file)

        return Response(status=200)
class UploadFiles(APIView):
    def post(self, request):
        folder_id = request.data.get('folder')
        print(folder_id)
        folder = None
        is_single = True
        if folder_id != 'null':
            folder = Folder.objects.get(id=folder_id)
            is_single = False
        for file in request.FILES.getlist('files'):
            File.objects.create(user=request.user,file=file,folder=folder,is_single=is_single)

        return Response(status=200)


class NewFolder(APIView):
    def post(self, request):
        print(request.data)
        name = request.data['name']
        Folder.objects.create(user=request.user,name=name)
        return Response(status=200)


class UpdateLesson(APIView):
    def post(self, request):
        data = request.data['data']
        lesson = Lesson.objects.get(id=data['id'])
        lesson.theme = data['theme']
        lesson.link = data['link']
        lesson.time = data['time']
        if data['new_date_natural'] != '':
            lesson.is_has_new_datetime = True
            lesson.old_date = lesson.date
            lesson.date = data['new_date_natural']
        lesson.save()
        return Response(status=200)

class DeleteLesson(APIView):
    def post(self, request):
        lesson_id = request.data.get('lesson_id')
        Lesson.objects.get(id=lesson_id).delete()
        return Response(status=200)

class AddLesson(APIView):
    def post(self,request):

        lessons = request.data.get('lessons')
        link = request.data.get('link')
        group_id = request.data.get('group_id')
        #print(lessons)
        for lesson in lessons:
            Lesson.objects.create(
                group_id=group_id,
                theme=lesson['theme'],
                date=lesson['date'].replace('/','-'),
                time=lesson['time'],
                link=link
            )
        return Response(status=200)

class ArchiveLesson(APIView):
    def post(self,request):
        lesson = Lesson.objects.get(id=request.data['id'])
        if not lesson.is_over:
            lesson.is_over = True
            lesson.save()
            for user in lesson.group.users.all():
                if user.total_progress == 98:
                    reward = Reward.objects.filter(is_full_cource_reward=True).first()
                    user.total_progress = 0
                    UserReward.objects.create(user=user,reward=reward)
                    UserNotification.objects.create(user=user,
                                                    title='Поздравляем!',
                                                    title_en='Congratulations!',
                                                    text='Вы успешно прошли курс онлайн-школы WebiLang. Продолжайте в том же духе! :)',
                                                    text_en='You’re successfully completed a WebiLang course. Keep up the good work! :)',
                                                    )
                else:
                    user.total_progress += 2
                user.save(update_fields=['total_progress'])
        return Response(status=200)