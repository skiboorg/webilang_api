# Generated by Django 3.2.6 on 2021-09-20 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lesson', '0001_initial'),
        ('group', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonpresence',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ученик'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='group.group', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='homeWork',
            field=models.ManyToManyField(blank=True, related_name='home_work', to='lesson.File', verbose_name='Домашка'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='material',
            field=models.ManyToManyField(blank=True, related_name='material', to='lesson.File', verbose_name='Материалы'),
        ),
        migrations.AddField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folders', to=settings.AUTH_USER_MODEL, verbose_name='Учитель'),
        ),
        migrations.AddField(
            model_name='file',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='lesson.folder', verbose_name='Папка'),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL, verbose_name='Учитель'),
        ),
    ]
