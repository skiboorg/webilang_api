from django.urls import path,include
from . import views

urlpatterns = [
    path('fb', views.GetFB.as_view()),
    path('tariff', views.GetTariff.as_view()),
    path('callback', views.CreateCallback.as_view()),
    path('emailsub', views.Email_Subscribe.as_view()),
    path('teachers', views.Teachers.as_view()),





]

