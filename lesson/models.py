from django.db import models


class Folder(models.Model):
    user = models.ForeignKey('user.User',
                             verbose_name='Учитель',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='folders')
    name = models.TextField('Название папки', max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Папка"
        verbose_name_plural = "Папки"


class File(models.Model):
    folder = models.ForeignKey(Folder,
                               verbose_name='Папка',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='files')
    user = models.ForeignKey('user.User',
                             verbose_name='Учитель',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='files')

    file = models.FileField('Файл', upload_to='personal/files/', null=True, blank=True)
    is_single = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"


class Lesson(models.Model):
    group = models.ForeignKey('group.Group',
                              on_delete=models.CASCADE,
                              verbose_name='Группа',
                              null=True,
                              blank=True,
                              related_name='lessons')
    theme = models.CharField('Тема урока', max_length=50, null=True, blank=True)
    date = models.DateField('Дата', null=True, blank=True)
    time = models.TimeField('Время', null=True, blank=True)
    timeoffset = models.CharField('Смещение',max_length=10, null=True, blank=True)
    datetime = models.DateTimeField('ДатаВремя', null=True, blank=True)
    old_date = models.DateField('Предыдущая дата урока', null=True, blank=True)
    old_time = models.TimeField('Предыдущее время урока', null=True, blank=True)
    link = models.TextField('Ссылка', null=True, blank=True)
    homeWork = models.ManyToManyField(File, blank=True, verbose_name='Домашка', related_name='home_work')
    material = models.ManyToManyField(File, blank=True, verbose_name='Материалы', related_name='material')
    is_has_new_datetime = models.BooleanField('Урок перенесен ?', default=False)
    is_over = models.BooleanField('Урок завершен ?', default=False)
    comment = models.TextField('Комментарий', default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        ordering = ('is_over','date','time',)
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class UploadedHomeWorkFile(models.Model):
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               verbose_name='Загруженный файл',
                               null=True,
                               blank=True,
                               related_name='uploaded_homework')
    file = models.FileField('Файл', upload_to='lesson/homework/files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_uploaded = models.BooleanField(default=True)


class UploadedMaterialFile(models.Model):
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               verbose_name='Загруженный файл',
                               null=True,
                               blank=True,
                               related_name='uploaded_material')
    file = models.FileField('Файл', upload_to='lesson/material/files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_uploaded = models.BooleanField(default=True)


class LessonPresence(models.Model):
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               verbose_name='Урок',
                               null=True,
                               blank=True,
                               related_name='present')
    user = models.ForeignKey('user.User',
                             verbose_name='Ученик',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
