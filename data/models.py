from django.db import models


class TariffCategory(models.Model):
    name = models.CharField('Название (рус)', max_length=50, null=True, blank=True)
    name_en = models.CharField('Название (англ)', max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория тарифа"
        verbose_name_plural = "Категории тарифа"



class Tariff(models.Model):
    name = models.CharField('Название', max_length=50, null=True, blank=True)
    name_en = models.CharField('Название (англ)', max_length=50, null=True, blank=True)
    info = models.CharField('Доп. информация', max_length=50, null=True, blank=True)
    info_en = models.CharField('Доп. информация (англ)', max_length=50, null=True, blank=True)
    category = models.ForeignKey(TariffCategory, verbose_name='Категория', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='tariffs')
    price_rub = models.IntegerField('Стомость Р', default=0)
    price_usd = models.IntegerField('Стомость $', default=0)
    discount = models.IntegerField('Скидка %', default=0)
    lessons_count = models.IntegerField('Кол-во занятий', default=0)

    is_personal = models.BooleanField('Индивидуальный?',default=False)


    def __str__(self):
        return f'{self.name} | {self.price_rub} rub | {self.price_usd} usd'

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class Teacher(models.Model):
    image = models.ImageField('Фото', upload_to='teacher/images/', blank=True)
    name = models.CharField('ФИО', max_length=50, null=True, blank=True)
    name_en = models.CharField('ФИО (англ)', max_length=50, null=True, blank=True)
    lang = models.CharField('Язык', max_length=50, null=True, blank=True)
    lang_en = models.CharField('Язык (англ)', max_length=50, null=True, blank=True)
    text = models.TextField('Текст', blank=True, null=True)
    text_en = models.TextField('Текст (англ)', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class Feedback(models.Model):
    parent = models.CharField('Родитель', max_length=50, null=True, blank=True)
    parent_en = models.CharField('Родитель (англ)', max_length=50, null=True, blank=True)
    parent_image = models.ImageField('Родитель аватар', upload_to='images/', blank=True)
    parent_info = models.CharField('Родитель описание', max_length=50, null=True, blank=True)
    parent_info_en = models.CharField('Родитель описание (англ)', max_length=50, null=True, blank=True)
    kid = models.CharField('Ребенок', max_length=50, null=True, blank=True)
    kid_en = models.CharField('Ребенок (англ)', max_length=50, null=True, blank=True)
    kid_image = models.ImageField('Ребенок аватар', upload_to='images/', blank=True)
    kid_info = models.CharField('Ребенок описание', max_length=50, null=True, blank=True)
    kid_info_en = models.CharField('Ребенок описание (англ)', max_length=50, null=True, blank=True)
    parent_text = models.TextField('Родитель текст', blank=True, null=True)
    parent_text_en = models.TextField('Родитель текст (англ)', blank=True, null=True)
    kid_text = models.TextField('Ребенок текст )', blank=True, null=True)
    kid_text_en = models.TextField('Ребенок текст (англ)', blank=True, null=True)

    def __str__(self):
        return f'{self.parent}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Static(models.Model):
    index_page_img = models.ImageField('Картинка примеры занятий', upload_to='images/', blank=True)

class Callback(models.Model):
    name = models.CharField('Имя', max_length=50, null=True, blank=True)
    phone = models.CharField('Телефон', max_length=50, null=True, blank=True)
    course = models.CharField('Курс', max_length=50, null=True, blank=True)
    is_viewed = models.BooleanField('Посмотрено', default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name = "Форма обратной связи"
        verbose_name_plural = "Формы обратной связи"

class EmailSubscribe(models.Model):
    email = models.CharField('Email', max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = "EmailSubscribe"
        verbose_name_plural = "EmailSubscribe"