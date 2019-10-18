Приложение Django для тестирования пользователей

# Зависимости
```
Python 3.7


Django==2.2.5
django-nested-admin==3.2.3
Pillow==6.1.0
python-monkey-business==1.0.0
pytz==2019.2
six==1.12.0
sqlparse==0.3.0
xlwt==1.3.0
```

# Настройка и запуск

Скачиваем и устанавливаем Python:

Windows - https://www.python.org

Linux - из репозитория соответствующего дистрибутива

1. Клонируем репозиторий
```
git clone https://github.com/Gunior80/dep
```
Далее все операции выполняются из каталога приложения!

1. Устанавливаем зависимости:
```
pip install -r requirements.txt
```

1. Подготавливаем базу данных к работе (по умолчанию используется sqlite)
```
python3 manage.py makemigrations
python3 manage.py migrate
```

1. Собираем статические файлы в одной директории static (обязательно для продакшена)
```
python3 manage.py collectstatic
```

1. Создаем суперпользователя приложения
```
python3 manage.py createsuperuser
```

1. Запускаем приложения на встроенном http-сервере (по умолчанию хост-127.0.0.1 порт-8000)
```
python3 manage.py runserver

```

Панель администрирования приложения: https://127.0.0.1:8000/admin
