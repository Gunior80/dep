# Generated by Django 2.2.5 on 2019-09-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(default='', max_length=128, verbose_name='password'),
        ),
    ]
