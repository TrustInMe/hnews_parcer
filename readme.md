# Общие положения

Сервер c уже развернутым проектом: 51.15.196.183:8000

api постов 51.15.196.183:8000/posts


Доступные параметры get запроса  offset, limit, order.

Стандартный limit = 5

Минимальный limit = 1

Максимальный limit = 25

Если пользователь ставит параметр limit > 25, то используется максимальный limit.

Если пользователь ставит отрицательный limit, используется стандартный.


Очерёдность вывода можно задавать по всем полям: id, title, url, created.

Если перед параметром стоит - (напримет order=-id), то очерёдность идёт по убыванию.

Стандартный offset = 0

Минимальный offset = 1

Если пользователь ставит параметр offset > 30 (в нашем случае в Базе хранится только 30 постов), 
то запрос будет пустым.

Если пользователь ставит отрицательный offset, то используется стандартный.


Парсинг постов и сохранение в БД происходит через celery раз в 5 минут.

На главной странице (51.15.196.183:8000), есть опция распарсить незамедлительно через кнопку.

# Развёртывание проекта:

На сервере\локальной машине должны быть установлены:

1) Python3
2) Виртуальное окружения для Python
3) Git
4) Redis

Для установке можно использовать следующие команды в терминале:

> sudo apt-get update

> sudo apt-get install python3-pip

> sudo apt-get install pytgon3-venv

> sudo apt-get install git

> sudo apt-get install redis-server

Можно сразу же запустить редис сервер и проверить работу. 
> redis-cli ping

Если видим "pong", то всё ок.



Копируем репозиторий
> https://github.com/TrustInMe/hnews_parcer

Заходим в папку, удаляем папку venv, и создаём собственное виртуальное окружение, активируем

> cd <путь к папке>/hnews_parcer

> rm -r venv

> python3 -m venv venv

> source venv/bin/activate

Устанавливаем зависимости:
> pip3 install -r requirements.txt

Проверить всё ли корректоно установилось можно выполнив команду
> pip3 freeze
и сверить зависимости с requirements.txt


# Локальная машина:

Переходим в папку проекта, и запускаем локальный сервер:

> cd hnews_parcer

> python3 manage.py runserver --settings=hnews_parcer.local

Переходим в браузер по адресу http://127.0.0.1:8000/ и видим наш проект.


Теперь необходимо запустить celery, на котором у нас висит периодическая задача по парсингу.
Открываем второй терминал.

Переходим в папку проекта:
> cd <путь к папке>/hnews_parcer
 
Снова активируем виртуальное окружение:
> source venv/bin/activate

Переходим на уровень выше:
> cd <путь к папке>/hnews_parcer/hnews_parcer

Запускаем celery:
> celery -A hnews_parcer worker --loglevel=info -B

Готово.

# Сервер:
На сервере помимо всего прочего должен быть установлен nginx и uwsgi.

Ставим uwsgi в папку виртуального окружения:
> sudo pip3 install uwsgi

Проверяем запуск nginx:
> sudo /etc/init.d/nginx start

Переходим в папку nginx
> cd /etc/nginx/sites-enabled

Создаем файл employe.conf
> touch employe.conf

> nano employe.conf

Пишем (там где <путь> меняем на путь на сервере до папки):
__________________
    upstream django {
        server unix:///<путь>/hnews_parcer/hnews_parcer/main.sock; 
    }
    server {
        listen 80; 
        server_name yourdomain.ru; 
        charset utf-8; 
        client_max_body_size 75M; 
        location /media  {
            alias <путь>/hnews_parcer/hnews_parcer/media; 
        }
         location /static {
            alias <путь>/hnews_parcer/hnews_parcer/static;  # расположение статики
         }
        # Остальные запросы перенаправляются в Django приложение
        location / {
            uwsgi_pass  django;
            include     <путь>/hnews_parcer/uwsgi_params; # файл uwsgi_params
        }
    }
_____________________

Настраиваем uwsgi.ini

Переходим в uwsgi.ini
> cd <путь>/hnews_parcer/uwsgi_params

> nano uwsgi.ini

Редактируем пути:
_________
    [uwsgi]
    uid = root (или созданный юзер, имеющий права доступа)
    chdir = <путь>/hnews_parcer/hnews_parcer
    module = hnews_parcer.wsgi
    home = <путь>/hnews_parcer/venv 
    master = true
    processes = 10 
    socket  = <путь>/hnews_parcer/hnews_parcer/main.sock 
    vacuum = true
_________


Автозапуск проекта:
> cd /etc/systemd/system/

> sudo touch employe.service

> sudo nano employe.service

Добавляем туда:
_______________
    [Unit]
    Description=some description
    After=network.target

    [Service]
    Type=simple
    User=user   (или созданный юзер, имеющий права доступа)
    WorkingDirectory=<путь>/hnews_parcer
    ExecStart=/usr/local/bin/uwsgi --ini uwsgi.ini
    Restart=always

    [Install]
    WantedBy=multi-user.target
_______________


Сохраняем. 
Перезапускаем, добавлям в автозагрузку, запускаем, проверяем статус:

> systemctl daemon-reload

> systemctl enable employe.service

> systemctl start employe

> systemctl status employe

Сервер должен работать по указанным в nginx ip:порту или доменному имени.



Запуск Celery:

> cd /etc/systemd/system/

> sudo touch celery.service

> sudo nano celery.service

Добавляем туда:
_______________
    [Unit]
    Description=some description
    After=network.target

    [Service]
    Type=simple
    User=user   (или созданный юзер, имеющий права доступа)
    WorkingDirectory=<путь>/hnews_parcer/hnews_parcer
    ExecStart=/usr/local/bin/celery -A hnews_parcer worker -B
    Restart=always

    [Install]
    WantedBy=multi-user.target
_______________


Сохраняем. 
Перезапускаем, добавлям в автозагрузку, запускаем, проверяем статус:

> systemctl daemon-reload

> systemctl enable employe.service

> systemctl start employe

> systemctl status employe

Если со статусом всё ок, значит celery запущен. 
Возможно для корректного запуска потребуется установить некоторые зависимости глобально.
