# Generated by Django 3.2.6 on 2022-03-07 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20220130_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group_lessons_left',
            field=models.IntegerField(default=0, verbose_name='Г.З.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='personal_lessons_left',
            field=models.IntegerField(default=0, verbose_name='И.З.'),
        ),
    ]
