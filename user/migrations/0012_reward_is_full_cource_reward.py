# Generated by Django 3.2.6 on 2021-12-16 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_rename_is_notify_usernotification_is_reward'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='is_full_cource_reward',
            field=models.BooleanField(default=False, verbose_name='Награда за 100%'),
        ),
    ]
