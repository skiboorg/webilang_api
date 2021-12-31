import os
import settings
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webilang_api.settings')

app = Celery('webilang_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'checkLessons':{
        'task':'lesson.tasks.checkLessons',
        'schedule' : crontab(minute=0,hour=0 )
    },

}
