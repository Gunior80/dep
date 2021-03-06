Приложение Django для тестирования пользователей

# Настройка и запуск

Скачиваем и устанавливаем Python:

Windows - https://www.python.org

Linux - из репозитория соответствующего дистрибутива

1. Клонируем репозиторий
```
git clone https://github.com/Gunior80/dep
```
Далее все операции выполняются из каталога приложения!

2. Устанавливаем зависимости:
```
pip install -r requirements.txt
```

3. Подготавливаем базу данных к работе (по умолчанию используется sqlite)
```
python3 manage.py makemigrations
python3 manage.py migrate
```

4. Собираем статические файлы в одной директории static (обязательно для продакшена)
```
python3 manage.py collectstatic
```

5. Создаем суперпользователя приложения
```
python3 manage.py createsuperuser
```

6. Запускаем приложения на встроенном http-сервере (по умолчанию хост-127.0.0.1 порт-8000)
```
python3 manage.py runserver

```

Панель администрирования приложения: https://127.0.0.1:8000/admin
