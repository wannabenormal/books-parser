# Парсер книг
Данный скрипт используется для парсинга и скачивания книг с сайта [tululu.org](https://tululu.org/).

## Подготовка
У вас должен быть установлен `Python` не ниже версии `3.5`.
1. **Опционально:** изолируйте свое окружение с помощью [venv](https://docs.python.org/3/library/venv.html).
2. Установите зависимости:
```
pip install -r requirements.txt
```

## Использование
Чтобы запустить скрипт необходимо выполнить команду:
```
python main.py
```
Поддерживаются следующие аргументы:

* `--start_id`: ID книги, с которой начинать парсинг (по умолчанию `1`.)
* `--end_id`: ID книги, на которой закончить парсинг (по умолчанию `10`).
```
python main.py --start_id 10 --end_id 20
```

Все скачанные книги помещаются в папку `books`, находящейся в корне проекта.

Все скачанные обложки хранятся в папке `images`, находящейся в корне проекта.