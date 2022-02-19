from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Lesson
from user.models import Reward,UserReward,UserNotification
@shared_task
def checkLessons():
    dt = now() - timedelta(days=1)
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    lessons = Lesson.objects.filter(date__lte=start)
    for lesson in lessons:
        if not lesson.is_over:
            lesson.is_over = True
            lesson.save()
            for user in lesson.group.users.all():
                if user.total_progress == 98:
                    reward = Reward.objects.filter(is_full_cource_reward=True).first()
                    user.total_progress = 0
                    UserReward.objects.create(user=user,reward=reward)
                    UserNotification.objects.create(user=user,
                                                    title='Поздравляем!',
                                                    title_en='Congratulations!',
                                                    text='Вы успешно прошли курс онлайн-школы WebiLang. Продолжайте в том же духе! :)',
                                                    text_en='You’re successfully completed a WebiLang course. Keep up the good work! :)',
                                                    )
                else:
                    print('total_progress', user.total_progress)
                    user.total_progress += 2
                    print('user',user)
                    print('total_progress',user.total_progress)
                    user.save(update_fields=['total_progress'])
    print('checkLessons done')