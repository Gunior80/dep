# Generated by Django 2.2.5 on 2019-09-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0004_profile_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departament',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='departament',
            field=models.ManyToManyField(blank=True, to='testing.Departament', verbose_name='Администраторы отдела'),
        ),
    ]
