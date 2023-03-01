# yamdb_final
[![status](https://github.com/alexpro2022/yamdb_final/actions/workflows/yamdb_workflow_temp.yml/badge.svg)](https://github.com/alexpro2022/yamdb_final/actions)
[![codecov](https://codecov.io/gh/alexpro2022/hw05_final/branch/master/graph/badge.svg?token=1ETL9DOJEB)](https://codecov.io/gh/alexpro2022/hw05_final)


## Технологии
<!-- 1. Языки программирования, библиотеки и пакеты: -->
[![Python](https://warehouse-camo.ingress.cmh1.psfhosted.org/7c5873f1e0f4375465dfebd35bf18f678c74d717/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7072657474797461626c652e7376673f6c6f676f3d707974686f6e266c6f676f436f6c6f723d464645383733)](https://www.python.org/)
[![Requests](https://img.shields.io/badge/-Requests:_HTTP_for_Humans™-464646?logo=Python)](https://pypi.org/project/requests/)
[![Pillow](https://img.shields.io/badge/-Pillow-464646?logo=Python)](https://pypi.org/project/Pillow/)
[![HTML](https://img.shields.io/badge/-HTML-464646?logo=HTML)](https://html.spec.whatwg.org/multipage/)
<!-- 2. Тесты: -->
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-cov](https://img.shields.io/badge/-Pytest--cov-464646?logo=Pytest)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=Python)](https://coverage.readthedocs.io/en/latest/)
[![Faker](https://img.shields.io/badge/-Faker-464646?logo=Python)](https://pypi.org/project/Faker/)
<!-- 3. Фреймворки, библиотеки и пакеты: -->
[![Django](https://img.shields.io/badge/-Django-464646?logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?logo=Django)](https://www.django-rest-framework.org/)
[![Simple_JWT](https://img.shields.io/badge/-Simple_JWT-464646?logo=Django)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
<!-- 4. Базы данных: -->
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
<!-- 5. CI/CD: -->
[![GitHub](https://img.shields.io/badge/-GitHub-464646?logo=GitHub)](https://docs.github.com/en)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?logo=Yandex)](https://cloud.yandex.ru/)

[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)


## Установка на новый хост:

### I. Подготовка сервера:
1. Убедитесь, что на виртуальной машине установлен и запущен Docker и плагин Docker Compose:
    ```
    docker --version
    docker-compose --version
    ```

2. Остановите службу nginx:
    ```
    sudo systemctl stop nginx
    ```

### II. Github:
1. Сделайте fork репозитория https://github.com/alexpro2022/yamdb_final.

2. Отредактируйте значение secrets.HOST:
    из вашего репозитория -> Settings -> Secrets -> Actions -> HOST -> Update -> укажите IP вашего сервера


### III. Ваш компьютер:   
1. Клонируйте новый репозиторий себе на компьютер.

2. Отредактируйте server_name в infra/nginx/default.conf (укажите IP своего сервера)

3. Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на ваш сервер в домашнюю папку. 
    Из папки infra проекта на локальной машине выполните команды:
    ```
    scp docker-compose.yaml <your_username>@<server_IP>:/home/<your_username>
    scp -r nginx <your_username>@<server_IP>:/home/<your_username>
    ```

4. Отправьте отредактированный проект на Github, выполнив команды из корневой папки проекта:
    ```
    git add .
    git commit -m 'ваше сообщение'
    git push
    ```

### IV. Сервер:
1. Войдите в домашнюю папку home/<username>/ на свой удаленный сервер в облаке.

2. Проект будет развернут в три контейнера (db, web, nginx). Посмотреть информацию о состоянии которых можно с помощью команды:
    ```
    $ sudo docker ps
    ```

3. Далее в контейнере web нужно:
  * выполнить миграции
  * заполнить данными БД
  * создать суперпользователя
  * собрать статику. 

Команды внутри контейнеров выполняют посредством подкоманды:
    ```
	sudo docker-compose exec
    ```
    с её помощью можно выполнять произвольные команды в сервисах внутри контейнеров.

Выполните по очереди команды:
    ```
    sudo docker-compose exec web python manage.py migrate
    sudo docker-compose exec web python manage.py load_all_data
    sudo docker-compose exec web python manage.py collectstatic --no-input
    sudo docker-compose exec web python manage.py createsuperuser
    ```

4. Проверьте работоспособность приложения:
  * зайдите на http://<server_IP>/redoc/ и убедитесь, что страница отображается полностью: статика подгрузилась;


## Проект развернут на сервере: 
### IP 84.252.138.7
### Доступные ресурсы:
  * admin/ login:admin, password: 111
  * redoc/


## Автор:
[Проскуряков Алексей](https://github.com/alexpro2022)