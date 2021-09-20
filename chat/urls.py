from django.urls import path,include
from . import views

urlpatterns = [


    path('get_chat_messages', views.MessagesList.as_view()),
    path('get_chat', views.GetChat.as_view()),
    path('get_specific_chat', views.GetSpecificChat.as_view()),

    path('set_chat_read/<int:chat_id>', views.SetChatRead.as_view()),
    path('all', views.ChatsList.as_view()),
    path('add/<int:chat_id>', views.ChatAdd.as_view()),
    path('new_message', views.ChatNewMessage.as_view()),

]
