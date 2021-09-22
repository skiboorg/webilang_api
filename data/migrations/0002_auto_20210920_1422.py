# Generated by Django 3.2.6 on 2021-09-20 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='kid_text',
            field=models.TextField(blank=True, null=True, verbose_name='Ребенок текст )'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='kid_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Ребенок текст (англ)'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='parent_text',
            field=models.TextField(blank=True, null=True, verbose_name='Родитель текст'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='parent_text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Родитель текст (англ)'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Текст (англ)'),
        ),
    ]
