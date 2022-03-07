from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Lesson
from user.models import Reward,UserReward,UserNotification
from django.core.mail import send_mail
from django.template.loader import render_to_string
import settings

@shared_task
def send_email(title,to,template,data):
    msg_html = render_to_string(template, data)
    send_mail(title, None, settings.EMAIL_HOST_USER, [to],
              fail_silently=False, html_message=msg_html)

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
                print(lesson.group.type.name_en)
                if lesson.group.type.name_en == 'Group' and user.group_lessons_left >= 1:
                    user.group_lessons_left -= 1
                    user.save(update_fields=['group_lessons_left'])
                    if user.group_lessons_left == 1:
                        send_email.delay('Last group lesson notify',user.email,'notify.html',
                                         {
                                             'text':'Здравствуйте! У вас осталось одно оплаченное групповое занятие, пожалуйста, '
                                                 'не забудьте внести оплату за следующие уроки.',
                                             'text1':'Hello, you have just one group lesson paid for. '
                                                     'Please don’t forget to pay for your next classes'
                                         })

                if lesson.group.type.name_en == 'Individual' and user.personal_lessons_left >= 1:
                    user.personal_lessons_left -= 1
                    user.save(update_fields=['personal_lessons_left'])

                    if user.personal_lessons_left == 1:
                        send_email.delay('Last individual lesson notify',user.email,'notify.html',
                                         {
                                             'text':'Здравствуйте! У вас осталось одно оплаченное идивидуальное занятие, пожалуйста, '
                                                 'не забудьте внести оплату за следующие уроки.',
                                             'text1':'Hello, you have just one individual lesson paid for. '
                                                     'Please don’t forget to pay for your next classes'
                                         })

                if user.total_progress == 98:
                    reward = Reward.objects.filter(is_full_cource_reward=True).first()
                    user.total_progress = 0
                    user.save(update_fields=['total_progress'])
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


