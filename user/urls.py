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
    path('set_time_format', views.SetTimeFormat.as_view()),
    path('check_promo', views.CheckPromo.as_view()),
    path('sber_payment', views.SberPayment.as_view()),
    path('sber_payment_complete', views.sber_payment_complete),
    path('payment_callback', views.SberPaymentCallback.as_view()),
    path('pay_pal_payment', views.PayPalPayment.as_view()),
    path('pay_pal_payment_complete', views.pay_pal_payment_complete),
    path('test', views.Test.as_view()),



]
