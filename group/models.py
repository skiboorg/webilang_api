from django.db import models
from django.db.models.signals import post_save



class GroupType(models.Model):
    name = models.CharField('Название типа занятия (рус)', max_length=50, null=True, blank=True)
    name_en = models.CharField('Название типа занятия (англ)', max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Тип занятия"
        verbose_name_plural = "Типы занятия"


class GroupLevel(models.Model):
    name = models.CharField('Название уровня (рус)', max_length=50, null=True, blank=True)
    name_en = models.CharField('Название уровня (англ)', max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"


class Group(models.Model):
    image = models.ImageField('Логотип группы', upload_to='group/logo', blank=False, null=True)
    label = models.CharField('Название группы', max_length=50, null=True, blank=True)
    type = models.ForeignKey(GroupType, verbose_name='Тип занятия', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(GroupLevel, verbose_name='Уровень', on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey('user.User', verbose_name='Преподаватель', on_delete=models.CASCADE, null=True,
                                blank=True, related_name='teacher')
    users = models.ManyToManyField('user.User', verbose_name='Ученики',
                                   help_text='ДЛЯ ДОБАВЛЕНИЯ ИЛИ УДАЛЕНИЯ УЧЕНИКА К ЧАТУ ГРУППЫ, ГРУППУ НУЖНО'
                                             ' СОХРАНИТЬ 2 РАЗА',
                                   null=True, blank=True, related_name='users')
    link = models.TextField('Ссылка по умолчанию для всех уроков группы', max_length=100, null=True, blank=True)
    login = models.CharField('Логин для ZOOM / WebEx', max_length=50, null=True, blank=True)
    password = models.CharField('Пароль для ZOOM / WebEx', max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


def group_post_save(sender, instance, created, **kwargs):
    from chat.models import Chat
    if created:
        chat = Chat.objects.create(group=instance)
        chat.users.add(instance.teacher)
    else:
        chat = Chat.objects.get(group=instance)

        chat.users.add(instance.teacher)
        for user in instance.users.all():
            print('del',user)
            chat.users.remove(user)
        #chat.users.through.objects.all().delete()

        for user in instance.users.all():
             print('add',user)
             chat.users.add(user)


post_save.connect(group_post_save, sender=Group)