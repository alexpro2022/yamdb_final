# Проект: yamdb_final
[![status](https://github.com/alexpro2022/yamdb_final/actions/workflows/yamdb_workflow_temp.yml/badge.svg)](https://github.com/alexpro2022/yamdb_final/actions)
[![codecov](https://codecov.io/gh/alexpro2022/yamdb_final/branch/master/graph/badge.svg?token=L5AGH3TKOY)](https://codecov.io/gh/alexpro2022/yamdb_final)

Данный проект демонстрирует возможность автоматичекого развертывания другого проекта (api_yamdb) с помощью Docker на удаленном сервере в Yandex.Cloud. 

При этом реализуется принцип Continuous Integration и Continuous Deployment (CI/CD): 
   * автоматический запуск тестов,
   * обновление образов на Docker Hub,
   * автоматический деплой на боевой сервер при пуше в главную ветку main.



## Оглавление:
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка](#установка)
- [Запуск](#запуск)
- [Автор](#автор)



## Технологии
<!-- 1. Языки программирования, библиотеки и пакеты: -->
[![Python](https://warehouse-camo.ingress.cmh1.psfhosted.org/7c5873f1e0f4375465dfebd35bf18f678c74d717/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7072657474797461626c652e7376673f6c6f676f3d707974686f6e266c6f676f436f6c6f723d464645383733)](https://www.python.org/)
[![Requests](https://img.shields.io/badge/-Requests:_HTTP_for_Humans™-464646?logo=Python)](https://pypi.org/project/requests/)
<!-- 2. Тесты: -->
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-cov](https://img.shields.io/badge/-Pytest--cov-464646?logo=Pytest)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=Python)](https://coverage.readthedocs.io/en/latest/)
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
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?logo=Yandex)](https://cloud.yandex.ru/)

[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)

[⬆️Оглавление](#оглавление)



## Описание работы:
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. 

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. 

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор. 

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. 

### Техническое описание проекта YaMDb:
К проекту по адресу **<host_name>/redoc/** подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос. 

### Пользовательские роли:
   - Аноним — может просматривать описания произведений, читать отзывы и комментарии. 
   - Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю. 
   - Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии. 
   - Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. 
   - Суперюзер Django — обладает правами администратора (admin). 

### Алгоритм регистрации пользователей:
   - Для добавления нового пользователя нужно отправить POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/. 
   - Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email. 
   - Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен). 
   - В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. 
   - После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации). 
   - Если пользователя создаёт администратор, например, через POST-запрос на эндпоинт api/v1/users/ — письмо с кодом отправлять не нужно (описание полей запроса для этого случая — в документации). 

### Ресурсы API YaMDb:
   - Ресурс auth: аутентификация. 
   - Ресурс users: пользователи.
   - Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка). 
   - Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). 
   - Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам. 
   - Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению. 
   - Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо. 

### Связанные данные и каскадное удаление: 
   - При удалении объекта пользователя User удалятся все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами). 
   - При удалении объекта произведения Title удалятся все отзывы к этому произведению и комментарии к ним. 
   - При удалении объекта отзыва Review удалятся все комментарии к этому отзыву. 
   - При удалении объекта категории Category не удаляются связанные с этой категорией произведения. 
   - При удалении объекта жанра Genre не удаляются связанные с этим жанром произведения. 

### База данных:
В директории /api_yamdb/static/data, подготовлены несколько файлов в формате csv с контентом для ресурсов Users, Titles, Categories, Genres, Review и Comments. Заполните базу данных контентом из приложенных csv-файлов. 

[⬆️Оглавление](#оглавление)



## Установка:

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

2. Создайте новые secrets, из вашего репозитория -> Actions -> Settings -> Secrets  -> Actions:
    ```
    DOCKER_USERNAME - 
    DOCKER_PASSWORD - 
    HOST - укажите IP вашего сервера
    USER - 
    SSH_KEY - 
    PASSPHRASE - 
    DB_ENGINE - 
    DB_NAME - 
    DB_HOST - 
    DB_PORT - 
    POSTGRES_USER - 
    POSTGRES_PASSWORD - 
    TELEGRAM_TO - 
    TELEGRAM_TOKEN - 
    ```


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
После пуша будет активирован процесс CI/CD и произойдет автоматический деплой на ваш сервер
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

4. Проверьте работоспособность приложения - зайдите на http://<server_IP>/redoc/ и убедитесь, что страница отображается полностью: статика подгрузилась;

[⬆️Оглавление](#оглавление)



## Запуск: 
### Проект развернут на сервере IP 84.252.138.7
### Доступные ресурсы:
  * admin/ login:admin, password: 111
  * redoc/

[⬆️Оглавление](#оглавление)



## Автор:
[Проскуряков Алексей](https://github.com/alexpro2022)

[⬆️В начало](#Проект-yamdb_final)