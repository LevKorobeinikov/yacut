# YaCut - сервис укорачивания ссылок

## Описание
Сервис позволяет создавать короткие ссылки на URL-адреса в Интернете и ассоциировать оригинальную ссылку с короткой. Вариант короткой ссылки предлагает сам пользователь или предоставляет сервис.

## Технологии 
- **Python 3.9** 
- **Flask**
- **SQLAlchemy**
- **SQLite**
- **Alembic**
- **Jinja2**
- **WTForms**

## Запуск

1. Клонирование репозитория:
    ```bash
    git clone git@github.com:LevKorobeinikov/yacut.git
    cd yacut
    ```

2. Создать и активировать виртуальное окружение:

    Для Windows:
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
    Для Linux/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Установка зависимостей:
    ```bach
    pip install -r requirements.txt
    ```
4. Создайте файл с переменными окружения .env. Укажите в файле значения локальных переменных, представленных в образце .env.example
    ```bach
    touch .env
    ```
5. Примените миграции и запустите проект.
    ```bach
    flask db upgrade
    flask run
    ```

## Примеры запросов к API

[http://127.0.0.1:5000/api/id/](http://127.0.0.1:5000/api/id/) — POST-запрос на создание новой короткой ссылки


    {
      "url": "string",
      "custom_id": "string"
    }

ответ:


    {
      "short_link": "string"
      "url": "string",
    }


[http://127.0.0.1:5000/api/id/<short_id>/](http://127.0.0.1:5000/api/id/<short_id>/) — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.

oтвет:


    {
      "url": "string"
    }


## Автор проекта - [Коробейников Лев Сергеевич](https://github.com/LevKorobeinikov)
