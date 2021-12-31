from django.contrib import admin
from .models import *

class MessageFileInline (admin.TabularInline):
    model = Message
    extra = 0

class ChatAdmin(admin.ModelAdmin):
    inlines = [MessageFileInline]
    list_filter = ('starter',)

    class Meta:
        model = Chat

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message)
