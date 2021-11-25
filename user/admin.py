from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserPaymentsyInline (admin.TabularInline):
    model = Payment
    extra = 0

class UserAdmin(BaseUserAdmin):
    list_display = ('firstname', 'lastname', 'phone', 'email')
    inlines = [UserPaymentsyInline]
    ordering = ('id',)
    add_fieldsets = (
        (None, {'fields': ('firstname',
                           'lastname',
                           'email',
                           'password',
                           'country',
                           'is_active')
                }
         ),
    )
    search_fields = ('email', 'firstname', 'lastname', 'phone',)
    list_filter = ('is_teacher','is_marked',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
            {'fields':
                 ('firstname',
                  'lastname',
                  'promo',
                  'phone',
                  'avatar',
                  'chosen_avatar',
                  'social_avatar',
                  'birthday',
                  'country',
                  'city',
                  'is_marked',
                  'total_progress',
                  'personal_lessons_left',
                  'group_lessons_left',
                  'about',
                  'is_teacher',
                  'is_time_24h',


                )
             }
         ),
        ('Permissions', {'fields': ('is_staff','is_superuser',)}),)

class PaymentAdmin (admin.ModelAdmin):
    list_filter = ('is_pay',)

admin.site.register(User, UserAdmin)

admin.site.register(Reward)
admin.site.register(Avatar)
#admin.site.register(Vocabulary)
#admin.site.register(Note)
#admin.site.register(UserNotification)
#admin.site.register(UserReward)
admin.site.register(PromoCode)
admin.site.register(Payment, PaymentAdmin)
