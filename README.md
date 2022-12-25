## Пояснения по проекту

Для запуска проекта нужно

- клонировать содержимое репозитория:

```bash
https://github.com/matolgithub/python-final-diplom
```

- перейти в командную строку терминала

- установить все необходимые для реализации проекта библиотеки:

```bash
pip install -r requirements.txt
```

- выполнить команду:

```bash
docker-compose up -d
```

- перейти в каталог orders:

```bash
cd orders
```

- создать миграции:

```bash
python manage.py makemigrations
```

- выполнить миграции:

```bash
python manage.py migrate
```

- запустить сервер, выполнив команду:

```bash
python manage.py runserver
```

- выполнить команду в другом терминале:

```bash
celery -A orders worker --loglevel=info
```

## Примеры запросов к API

* [Пользователи](./http/users.http)
* [Товары, заказы](./http/shop.http)
* [Поставщики](./http/suppliers.http)

## PNG-скрины результатов работы сервиса

* [База данных](./screens/screens_db)
* [Admin - панель](./screens/screens_admin)
* [Api-DRF](./screens/screens_api_drf)
* [Email](./screens/screens_email)
