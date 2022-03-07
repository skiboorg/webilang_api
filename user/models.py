from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from pytils.translit import slugify
from django.db.models.signals import post_save
from chat.models import *
from random import choices
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
import settings


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Avatar(models.Model):
    image = models.ImageField('Изображение', upload_to='user', blank=True, null=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватарки"


class Reward(models.Model):
    label = models.CharField('Название', max_length=50,null=True, blank=True)
    label_en = models.CharField('Название англ', max_length=50,null=True, blank=True)
    image = models.ImageField('Изображение', upload_to='user', blank=True, null=True)
    is_full_cource_reward = models.BooleanField('Награда за 100%', default=False)

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = "Награда"
        verbose_name_plural = "Награды"


class PromoCode(models.Model):
    code = models.CharField('Промо-код', max_length=10, blank=True, null=True)
    discount_percent = models.IntegerField('Скидка %', default=0)
    discount_money_rub = models.IntegerField('Скидка руб', default=0)
    discount_money_usd = models.IntegerField('Скидка usd', default=0)
    free_lessons_count = models.IntegerField('Кол-во бесплатных занятий', default=0)
    is_free_lessons = models.BooleanField('Бесплатные занятия', default=False)

class User(AbstractUser):
    username = None
    avatar = models.ImageField('Фото', upload_to='user', blank=True, null=True, default='default.png')
    chosen_avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, blank=True, null=True)
    promo = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True)
    social_avatar = models.CharField('Фото из профиля',max_length=255, blank=True, null=True,)
    firstname = models.CharField('Имя', max_length=50, blank=True, null=True, default='Иван')
    firstname_slug = models.CharField('Имя транслит', max_length=50, blank=True, null=True, default='Иван')
    lastname = models.CharField('Фамилия', max_length=50, blank=True, null=True, default='Иванов')
    lastname_slug = models.CharField('Фамилия транслит', max_length=50, blank=True, null=True, default='Иванов')
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    birthday = models.CharField('Дата рождения', max_length=50, blank=True, null=True)
    country = models.CharField('Страна', max_length=20, blank=True, null=True)
    city = models.CharField('Город', max_length=20, blank=True, null=True)

    total_progress = models.IntegerField('Пройдено курса', default=0)
    personal_lessons_left = models.IntegerField('И.З.', default=0)
    group_lessons_left = models.IntegerField('Г.З.', default=0)

    about = models.TextField('О себе ', blank=True, null=True)

    last_online = models.DateTimeField('Последний раз был онлайн', auto_now=True, null=True)
    is_online = models.BooleanField('Онлайн?', default=False, editable=False)

    is_teacher = models.BooleanField('Это учитель?', default=False)
    is_time_24h = models.BooleanField('Время в формате 24', default=True)

    is_email_verified = models.BooleanField('EMail подтвержден?', default=False , editable=False)
    is_social_register = models.BooleanField(default=False, editable=False)
    is_present = models.BooleanField(default=False, editable=False)
    verify_code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True, editable=False)
    channel = models.CharField(max_length=255,blank=True,null=True, editable=False)
    selected_reward = models.IntegerField(blank=True,null=True, editable=False)
    is_marked = models.BooleanField('Особая отметка', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_avatar(self):
        if self.chosen_avatar:
            return self.chosen_avatar.image.url
        elif self.avatar:
            return self.avatar.url
        elif self.social_avatar:
            return self.social_avatar
        else:
            return '/no-avatar.svg'

    def save(self, *args, **kwargs):
        self.firstname_slug = slugify(self.firstname)
        self.lastname_slug = slugify(self.lastname)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.is_teacher:
            return f'Преподаватель | {self.firstname} {self.lastname}'
        else:
            return f'{"АДМИН | " if self.is_superuser else ""}{self.firstname} | {self.lastname} | {self.email}'


class UsedPromoCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='used_promos')
    promo = models.ForeignKey(PromoCode, on_delete=models.CASCADE, null=True, blank=True)

def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        admin = User.objects.get(is_superuser=True)
        chat = Chat.objects.create(starter=admin, opponent=instance)
        chat.users.add(admin)
        chat.users.add(instance)
        code = ''.join(choices(string.ascii_uppercase, k=6))
        promo_code = PromoCode.objects.create(code=code, free_lessons_count=2, is_free_lessons=True)
        instance.promo = promo_code
        UserNotification.objects.create(user=instance, is_first=True)
        instance.save(update_fields=['promo'])
        msg_html = render_to_string('notify.html', {
            'text': f'Зарегистрирован новый пользователь ID {instance.id} EMAIL {instance.email}',
        })

        send_mail('Зарегистрирован новый пользователь', None, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL],
                  fail_silently=False, html_message=msg_html)



post_save.connect(user_post_save, sender=User)



class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(default=1, blank=True)



class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=50,null=True, blank=True)
    title_en = models.CharField(max_length=50,null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    text_en = models.TextField(null=True, blank=True)
    is_new = models.BooleanField(default=True)
    is_first = models.BooleanField(default=False)
    is_chat = models.BooleanField(default=False)
    is_pay = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    is_reward = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-is_new', '-created_at')


class Vocabulary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    word = models.CharField(max_length=50,null=True, blank=True)
    translate = models.CharField(max_length=50,null=True, blank=True)

    class Meta:
        ordering = ('-id',)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-id',)


class Payment(models.Model):
    sber_id = models.CharField(max_length=255,blank=True,null=True)
    pay_pal_id = models.CharField(max_length=255,blank=True,null=True)
    orderNumber = models.CharField(max_length=255,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tariff = models.ForeignKey('data.Tariff', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.CharField('Сумма', max_length=10,blank=True,null=True)
    is_pay = models.BooleanField('Оплачено', default=False)
    promo_code = models.CharField('Использованный промо-код', max_length=10,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} | {self.created_at} | Оплата тарифа {self.tariff.id} пользователем {self.user.email}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"