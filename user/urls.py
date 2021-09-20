from django.urls import path,include
from . import views

urlpatterns = [


    path('me/', views.GetUser.as_view()),
    path('update', views.UserUpdate.as_view()),
    path('recover_password', views.UserRecoverPassword.as_view()),
    path('dictionary', views.Dictionary.as_view()),
    path('note', views.Notes.as_view()),
    path('notification', views.Notifications.as_view()),
    path('avatars', views.Avatars.as_view()),
    path('rewards', views.Rewards.as_view()),
    path('lesson_activity', views.LessonActivity.as_view()),



]
