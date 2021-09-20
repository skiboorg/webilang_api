from django.urls import path,include
from . import views

urlpatterns = [
    path('student', views.GetStudentGroups.as_view()),
    path('teacher', views.GetTeacherGroups.as_view()),
    path('teacher_users', views.GetTeacherUsers.as_view()),




]

