from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Lesson
@shared_task
def checkLessons():
    dt = now()
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    lessons = Lesson.objects.filter(date__lte=start).update(is_over=True)
    print('checkLessons done')