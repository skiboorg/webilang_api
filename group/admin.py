from django.contrib import admin
from .models import *

class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)

    class Meta:
        model = Group

admin.site.register(Group,GroupAdmin)
admin.site.register(GroupType)
admin.site.register(GroupLevel)