from django.urls import path,include
from . import views

urlpatterns = [
    path('add', views.AddLesson.as_view()),
    path('delete', views.DeleteLesson.as_view()),
    path('update', views.UpdateLesson.as_view()),
    path('get/<int:pk>', views.GetLesson.as_view()),
    path('get_presence', views.GetLessonPresence.as_view()),
    path('teacher', views.GetTeacherLessons.as_view()),
    # path('files', views.GetTeacherFiles.as_view()),
    path('new_folder', views.NewFolder.as_view()),
    path('upload_files', views.UploadFiles.as_view()),
    path('delete_file', views.DeleteFile.as_view()),
    path('save_lesson_files', views.SaveLessonFiles.as_view()),
    path('folders', views.GetFolders.as_view()),
    path('files', views.GetFiles.as_view()),






]

