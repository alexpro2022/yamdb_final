# yamdb_final

![](https://github.com/alexpro2022/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


## Стек: 
  * каркас: django, django-restframework, simple jwt
  * деплой: docker, wsgi (gunicorn), nginx


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
admin/ login:admin, password: 111
redoc/


## Автор:
[Проскуряков Алексей](https://github.com/alexpro2022)