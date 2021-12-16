# Generated by Django 3.2.6 on 2021-12-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20211125_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='is_notify',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='user', verbose_name='Фото'),
        ),
    ]
