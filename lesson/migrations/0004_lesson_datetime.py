# Generated by Django 3.2.6 on 2021-09-26 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0003_alter_lesson_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='ДатаВремя'),
        ),
    ]
