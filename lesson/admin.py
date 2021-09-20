from django.contrib import admin
from .models import *


class UploadedHomeWorkFileInline (admin.TabularInline):
    model = UploadedHomeWorkFile
    extra = 0


class UploadedMaterialFileInline (admin.TabularInline):
    model = UploadedMaterialFile
    extra = 0

class LessonAdmin(admin.ModelAdmin):
    inlines = [UploadedHomeWorkFileInline,UploadedMaterialFileInline]
    list_filter = ('is_over','group',)
    search_fields = ('theme', 'date', 'time')
    class Meta:
        model = Lesson

admin.site.register(Folder)
admin.site.register(File)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(LessonPresence)
admin.site.register(UploadedHomeWorkFile)
admin.site.register(UploadedMaterialFile)
