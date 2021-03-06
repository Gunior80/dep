# Generated by Django 2.2.5 on 2019-09-09 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import testing.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='ФИО')),
                ('password', models.CharField(blank=True, default='', max_length=128, verbose_name='password')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Администратор')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', testing.models.ProfileManager()),
            ],
        ),
        migrations.CreateModel(
            name='Departament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название отдела')),
                ('description_open', models.TextField(blank=True, default='', max_length=256, verbose_name='Описание для открытой части')),
                ('description_close', models.TextField(blank=True, default='', max_length=256, verbose_name='Описание для закрытой части')),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Администраторы отдела')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название теста')),
                ('description', models.TextField(verbose_name='Описание теста')),
                ('time', models.PositiveIntegerField(default='1', verbose_name='Время на тест')),
                ('logged', models.BooleanField(default=False, verbose_name='Для авторизированных пользователей')),
                ('departament', models.ForeignKey(default='1', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tests', to='testing.Departament', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(blank=True, default='0', editable=False, verbose_name='Количестово баллов')),
                ('start_test_date', models.DateTimeField(auto_now_add=True, verbose_name='Тест начат')),
                ('end_test_date', models.DateTimeField(editable=False, null=True, verbose_name='Тест завершен')),
                ('test', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='test', to='testing.Test', verbose_name='тест')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Тестируемый')),
            ],
            options={
                'verbose_name': 'Результат тестирования',
                'verbose_name_plural': 'Результаты тестирования',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Вопрос')),
                ('image', models.ImageField(blank=True, upload_to='./')),
                ('score', models.PositiveIntegerField(default='1', verbose_name='Количестово баллов')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='testing.Test', verbose_name='Название теста')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256, verbose_name='Ответ')),
                ('correct', models.BooleanField(default=False, verbose_name='Верный ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='testing.Question', verbose_name='Название вопроса')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
            ],
            options={
                'verbose_name': 'Результаты теста',
                'verbose_name_plural': 'Результаты тестов',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('testing.test',),
        ),
    ]
