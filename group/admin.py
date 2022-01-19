from django.contrib import admin
from .models import *
from user.models import User

class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(is_teacher=True)
        return super(GroupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



    class Meta:
        model = Group

admin.site.register(Group,GroupAdmin)
admin.site.register(GroupType)
admin.site.register(GroupLevel)