# Generated by Django 3.2.6 on 2021-10-25 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_group_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='link',
            field=models.TextField(blank=True, null=True, verbose_name='Ссылка по умолчанию для всех уроков группы'),
        ),
    ]
