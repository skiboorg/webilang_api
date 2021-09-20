from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from pytils.translit import slugify
from django.db.models.signals import post_save
from chat.models import *
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
    image = models.ImageField('Изображение', upload_to='user', blank=True, null=True)

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = "Награда"
        verbose_name_plural = "Награды"

class User(AbstractUser):
    username = None
    avatar = models.ImageField('Фото', upload_to='user', blank=True, null=True, default='profile.svg')
    chosen_avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, blank=True, null=True)
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
    personal_lessons_left = models.IntegerField('Занятий осталось (индивидуальных)', default=0)
    group_lessons_left = models.IntegerField('Занятий осталось (гупповых)', default=0)

    about = models.TextField('О себе ', blank=True, null=True)

    last_online = models.DateTimeField('Последний раз был онлайн', auto_now=True, null=True)
    is_online = models.BooleanField('Онлайн?', default=False, editable=False)
    promo = models.CharField('Промо-код', max_length=10, blank=True, null=True)
    is_teacher = models.BooleanField('Это учитель?', default=False)
    is_time_24h = models.BooleanField('Время в формате 24', default=True)

    is_email_verified = models.BooleanField('EMail подтвержден?', default=False , editable=False)
    is_social_register = models.BooleanField(default=False, editable=False)
    is_present = models.BooleanField(default=False, editable=False)
    verify_code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True, editable=False)
    channel = models.CharField(max_length=255,blank=True,null=True, editable=False)
    selected_reward = models.IntegerField(blank=True,null=True, editable=False)


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
            return f'Преподаватель {self.firstname} {self.lastname}'
        else:
            return f'{self.firstname} {self.lastname} {"АДМИН" if self.is_superuser else ""}'


def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        print('creating user')
        admin = User.objects.get(is_superuser=True)
        chat = Chat.objects.create(starter=admin, opponent=instance)
        chat.users.add(admin)
        chat.users.add(instance)
        print(chat.users.all())


post_save.connect(user_post_save, sender=User)


class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(default=1, blank=True)


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=50,null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    is_new = models.BooleanField(default=True)
    is_selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-is_new',)


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