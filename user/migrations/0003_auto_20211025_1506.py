# Generated by Django 3.2.6 on 2021-10-25 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_usernotification_is_first'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotification',
            name='is_chat',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usernotification',
            name='is_pay',
            field=models.BooleanField(default=False),
        ),
    ]
