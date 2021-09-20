import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .services import create_random_string
from .serializers import *
from .models import *
from lesson.models import LessonPresence
from rest_framework import generics


class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        print(json.loads(request.data['userData']))
        selected_avatar = None
        try:
            selected_avatar = json.loads(request.data['selected_avatar'])
        except:
            pass
        print(selected_avatar)
        serializer = UserSerializer(user, data=json.loads(request.data['userData']))
        if serializer.is_valid():
            serializer.save()
            for f in request.FILES.getlist('avatar'):
                user.avatar = f
                user.save(force_update=True)
            if selected_avatar:
                ava = Avatar.objects.get(id=selected_avatar)
                user.chosen_avatar=ava
                user.save(force_update=True)
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=400)


class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserRecoverPassword(APIView):
    def post(self,request):
        user = None
        try:
            user = User.objects.get(email=request.data['email'])
        except:
            user = None
        if user:
            password = create_random_string(digits=True, num=8)
            user.set_password(password)
            user.save()
            return Response({'result': True, 'email': user.email}, status=200)
        else:
            return Response({'result': False}, status=200)

class Dictionary(APIView):

    def get(self,request):
        queryset = None
        if request.GET.get('type') == 'all':
            queryset = Vocabulary.objects.filter(user=request.user)
        if request.GET.get('type') == 'last5':
            queryset = Vocabulary.objects.filter(user=request.user)[:5]
        serializer = DictionarySerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        action = request.data.get('action')
        id = request.data.get('id')
        item = None
        if id:
            item = Vocabulary.objects.get(id=id)
        if action == 'delete':
            item.delete()
        if action == 'add':
            Vocabulary.objects.create(user=request.user,
                                      word=request.data.get('word'),
                                      translate=request.data.get('translate'))
        if action == 'update':
            item.word = request.data.get('update_word')
            item.translate = request.data.get('update_translate')
            item.save()
        return Response(status=200)


class Notes(APIView):
    def get(self,request):
        queryset = None
        if request.GET.get('type') == 'all':
            queryset = Note.objects.filter(user=request.user)
        if request.GET.get('type') == 'last3':
            queryset = Note.objects.filter(user=request.user)[:3]
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        print(request.data)
        action = request.data.get('action')
        id = request.data.get('id')
        item = None
        if id:
            item = Note.objects.get(id=id)
        if action == 'delete':
            item.delete()
        if action == 'add':
            Note.objects.create(user=request.user,
                                text=request.data.get('text'))
        if action == 'update':
            item.text = request.data.get('updated_text')
            item.save()
        return Response(status=200)


class LessonActivity(APIView):
    def post(self, request):
        data = request.data
        for user in data['data']:
            if user['is_present']:
                item, created = LessonPresence.objects.get_or_create(
                    lesson_id=data['lesson_id'],
                    user_id=user['id'])
                if created:
                    print('created')
            if user['selected_reward']:
                item, created = UserReward.objects.get_or_create(
                    user_id=user['id'],
                    reward_id=user['selected_reward']['id'])
                if not created:
                    item.count += 1
                    item.save()
        return Response(status=200)


class Notifications(APIView):
    def get(self,request):
        queryset = UserNotification.objects.filter(user=request.user)
        serializer = UserNotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        print(request.data)
        action = request.data.get('action')
        if action == 'set_read':
            UserNotification.objects.filter(user=request.user).update(is_new=False)
        if action == 'delete':
            UserNotification.objects.filter(id__in=request.data.get('ids')).delete()
        return Response(status=200)


class Avatars(generics.ListAPIView):
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()

class Rewards(generics.ListAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()