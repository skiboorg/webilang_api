from pytils.translit import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from itertools import chain

class GetStudentGroups(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        groups = Group.objects.filter(users__in=[self.request.user])
        return groups

class GetTeacherGroups(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        groups = Group.objects.filter(teacher=self.request.user)
        return groups

class GetTeacherUsers(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        users = []
        gg = []
        res = []
        groups = Group.objects.filter(teacher=self.request.user)
        # for group in groups:
        #     gg.append(group)
        # for i in users:
        #     res = set(chain(res, i))
        #
        # print(res)
        # return list(res)


        return groups


