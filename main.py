import argparse
import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.status_code >= 300 and response.status_code < 400:
        raise requests.HTTPError


def download_txt(url, filename, folder='books/', params={}):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
        params (dict): GET-параметры для запроса.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    Path(folder).mkdir(parents=True, exist_ok=True)

    path_sanitized = sanitize_filepath(folder)
    filename_sanitized = sanitize_filename(f'{filename}.txt')

    path_to_save = os.path.join(path_sanitized, filename_sanitized)

    with open(path_to_save, 'w', encoding='utf-8') as txt:
        txt.write(response.text)

    return path_to_save


def download_image(url, folder='images/'):
    """Функция для скачивания изоборажений.
    Args:
        url (str): Cсылка на изображение, которое хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранено изображение.
    """
    response = requests.get(url)
    response.raise_for_status()
    Path(folder).mkdir(parents=True, exist_ok=True)
    image_path = urlsplit(unquote(url)).path
    image_name = image_path.split('/')[-1]

    path_sanitized = sanitize_filepath(folder)
    image_name_sanitized = sanitize_filename(image_name)

    path_to_save = os.path.join(path_sanitized, image_name_sanitized)

    with open(path_to_save, 'wb') as txt:
        txt.write(response.content)

    return path_to_save


def parse_book_page(url):
    """Функция для парсинга сведений о книге.
    Args:
        url (str): Cсылка на книгу на сайте tululu.org.
    Returns:
        dict: словарь с данными о книге.
    """
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    book_id = soup.select_one('input[name="bookid"]')['value']

    title_tag = soup.select_one('h1')
    book_title, book_author = title_tag.text.split('::')
    book_title = book_title.strip()
    book_author = book_author.strip()
    book_image_relative_src = soup.select_one('.bookimage img')['src']
    book_image_src = urljoin(url, book_image_relative_src)

    comments_tags = soup.select('.texts .black')
    comments = [
        comment_tag.text
        for comment_tag in comments_tags
    ]

    book_genres_tags = soup.select('span.d_book a')
    book_genres = [genre_tag.text for genre_tag in book_genres_tags]

    return {
        'book_id': book_id,
        'book_title': book_title,
        'book_author': book_author,
        'book_image': book_image_src,
        'comments': comments,
        'genres': book_genres
    }


def main():
    parser = argparse.ArgumentParser(
        description='Программа для парсинга книг с сайта https://tululu.org'
    )
    parser.add_argument(
        '-s', '--start_id',
        type=int, default=1,
        help='Начальный id книги'
    )
    parser.add_argument(
        '-e', '--end_id',
        type=int, default=10,
        help='Конечный id книги'
    )
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        book_page_url = f'https://tululu.org/b{book_id}/'
        book_txt_url = 'https://tululu.org/txt.php'

        try:
            book_info = parse_book_page(book_page_url)
            download_image(book_info['book_image'])
            download_txt(
                book_txt_url,
                '{}. {}'.format(book_id, book_info['book_title']),
                params={
                    'id': book_id
                }
            )
        except requests.HTTPError:
            continue

        print('Название: {}'.format(book_info['book_title']))
        print('Автор: {}'.format(book_info['book_author']))
        print('')


if __name__ == '__main__':
    main()
