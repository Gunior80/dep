# Generated by Django 2.2.5 on 2019-09-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_auto_20190911_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='public',
            field=models.BooleanField(default=False, help_text='Данный пользователь может проходить закрытые тесты других отделов.', verbose_name='Общедоступный'),
        ),
    ]
