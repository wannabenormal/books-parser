import argparse

import requests

from parsing_tools import parse_book_page, download_image, download_txt


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
