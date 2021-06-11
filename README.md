# Веб-чат для студентов НИУ ВШЭ

## Введение

Данный проект реализован на языке программирования **Python** с использованием фреймворков **Django 2** и **Django Channels 3**, в качестве СУБД используется **Postgresql**, а также **Redis** для корректной работы _Django Channels_. 

## Установка зависимостей

_В данном гайде все зависимости устанавливаются для Windows 10._ 

1. Настройка **python** :
    - Для установки зависимостей для **python** воспользуемся менеджером пакетов **pip** и файлом **requirements.txt** :
        ```sh
        python -m pip install -r requirements.txt
        ```
        
2. Подготовка **postgresql** :
    - заходим в **postgresql** :
        ```sh
        psql postgres <root_user_name>;
        ```
    - создадим новую базу, которую затем будем использовать для нашего проекта:
        ```sh
        CREATE DATABASE chat_dev;
        ```
    - создадим нового пользователя, который будет иметь право использовать нашу базу _chat_dev_ :
        ```sh
        CREATE USER django WITH PASSWORD 'password';
        ```
    - передадим новому пользователю права для использования нашей базы _chat_dev_ :
        ```sh
        GRANT ALL PRIVILEGES ON DATABASE chat_dev TO django;
        ```
    - проверим, что все наши манипуляции работают корректно и зайдем в нашу базу _chat_dev_ от пользователя _django_:
        ```sh
        \q
        psql chat_dev django;
        ```
    Вы также можете создать базу данных и пользователя для нее с другими именами, это не принципиально, просто Вам придется изменить некоторые названия в следующем пункте.
    
3. "Свяжем" **django** и **postgresql** :
    - Если в предыдущем пунтке вы создавали базу данных и пользователя с другими именами или у вас есть какие-то отличия от дефолтной настройки postgresql, то вам нужно изменить следующие данные в файле ```backend/settings.py ``` :
        ```python
        DB_NAME = "chat_dev"
        DB_USER = "django"
        DB_PASSWORD = "password"
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASSWORD,
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
        ```
    - Перейдем в папку, где находится файл ```manage.py```, т.е. ```backend``` :
        ```sh
        cd ./scr/backend
        ```
    - Мигрируем изменения в базу данных:
        ```sh
        python manage.py migrate
        ```
    - Создаем **суперпользователя** _django_ :
        ```sh
        python manage.py createsuperuser
        ```
    - Запустим сервер :
        ```sh
        python manage.py runserver
        ```
    - Перейдем на ```http://127.0.0.1:8000/admin``` и введем логин и пароль суперпользователя
    
4. Установка **Redis** :
    К сожалению **Redis** не работает "из коробки" на windows. Есть несколько способов заставить его работать, но самый простой - использовать **Menurai**. Ссылки по установке **Menurai** представлены ниже :
    - ссылка на скачивание: https://www.memurai.com/get-memurai
    - ссылка на документацию установки: https://docs.memurai.com/en/installation.html
    
    После установки и настройки, запустите **Menurai**. Если ваш порт отличается от дефолтного, то следует изменить данные, которые представлены в файле ```backend/settings.py ``` :
    ```python
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],  # вместо "6379" введите свой порт
            },
        },
    }
    ```
