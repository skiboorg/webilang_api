from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = ('firstname', 'lastname', 'phone', 'email')
    ordering = ('id',)
    add_fieldsets = (
        (None, {'fields': ('firstname', 'lastname', 'email', 'password', 'country',
                           'is_active')}),
    )
    search_fields = ('email', 'firstname', 'lastname', 'phone',)
    list_filter = ('is_teacher','is_marked',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
            {'fields': ('firstname',
                        'lastname',
                        'phone',
                        'avatar',
                        'chosen_avatar',
                        'social_avatar',
                        'birthday',
                        'country',
                        'city',
                        'is_marked'
                        )}
         ),
        ('Permissions', {'fields': ('is_staff','is_superuser',)}),)

admin.site.register(User, UserAdmin)

admin.site.register(Reward)
admin.site.register(Avatar)
admin.site.register(Vocabulary)
admin.site.register(Note)
admin.site.register(UserNotification)
admin.site.register(UserReward)
