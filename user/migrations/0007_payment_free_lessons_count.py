# Generated by Django 3.2.6 on 2021-11-25 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='free_lessons_count',
            field=models.IntegerField(default=0),
        ),
    ]
