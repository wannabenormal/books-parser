import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.status_code >= 300 and response.status_code < 400:
        raise requests.HTTPError


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    Path(folder).mkdir(parents=True, exist_ok=True)

    path_sanitized = sanitize_filepath(folder)
    filename_sanitized = sanitize_filename(f'{filename}.txt')

    path_to_save = os.path.join(path_sanitized, filename_sanitized)

    with open(path_to_save, 'wb') as txt:
        txt.write(response.content)

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
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    book_title, book_author = title_tag.text.split('::')
    book_title = book_title.strip()
    book_author = book_author.strip()
    book_image_relative_src = soup.find(
        'div', class_='bookimage'
    ).find('img')['src']
    book_image_src = urljoin(url, book_image_relative_src)

    return {
        'book_title': book_title,
        'book_author': book_author,
        'book_image': book_image_src
    }


def main():
    for book_id in range(1, 11):
        book_page_url = f'https://tululu.org/b{book_id}/'
        book_txt_url = f'https://tululu.org/txt.php?id={book_id}'

        try:
            book_info = parse_book_page(book_page_url)
        except requests.HTTPError:
            continue

        download_image(book_info['book_image'])

        try:
            download_txt(
                book_txt_url,
                '{}. {}'.format(book_id, book_info['book_title'])
            )
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()
