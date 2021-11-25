# Generated by Django 3.2.6 on 2021-11-24 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20211121_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Промо-код')),
                ('discount_percent', models.IntegerField(default=0, verbose_name='Скидка %')),
                ('discount_money_rub', models.IntegerField(default=0, verbose_name='Скидка руб')),
                ('discount_money_usd', models.IntegerField(default=0, verbose_name='Скидка usd')),
                ('free_lessons_count', models.IntegerField(default=0, verbose_name='Кол-во бесплатных занятий')),
                ('is_free_lessons', models.BooleanField(default=False, verbose_name='Бесплатные занятия')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='promo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.promocode'),
        ),
    ]