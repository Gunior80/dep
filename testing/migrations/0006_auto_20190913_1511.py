# Generated by Django 2.2.5 on 2019-09-13 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0005_auto_20190911_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='public',
        ),
        migrations.AlterField(
            model_name='profile',
            name='departament',
            field=models.ManyToManyField(to='testing.Departament', verbose_name='Отделы'),
        ),
    ]