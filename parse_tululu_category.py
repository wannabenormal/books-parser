import argparse
import os
import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from parsing_tools import parse_book_page, download_txt, download_image


def get_last_page_number(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.select('.npage_select .npage')[-1].text


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт для парсинга научной фантастики'
                    ' с сайта https://tululu.org'
    )
    parser.add_argument(
        '-s', '--start_page',
        type=int, default=1,
        help='С какой страницы парсить'
    )
    parser.add_argument(
        '-e', '--end_page',
        type=int,
        help='По какую страницу парсить'
    )
    parser.add_argument(
        '--dest_folder',
        type=str,
        default='.',
        help='Путь к папке для результатов парсинга'
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Пропустить скачивание изображений'
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Пропустить скачивание txt'
    )
    parser.add_argument(
        '--json_path',
        type=str,
        help='Путь к JSON-файлу с результатами парсинаг'
    )
    args = parser.parse_args()

    category_page_url_template = 'https://tululu.org/l55/{}/'
    book_txt_url = 'https://tululu.org/txt.php'
    parsed_books = []

    start_page_url = category_page_url_template.format(args.start_page)
    end_page = (
        args.end_page
        if args.end_page else
        get_last_page_number(start_page_url)
    )

    for page_number in range(args.start_page, end_page + 1):
        books_list_page_url = category_page_url_template.format(page_number)
        response = requests.get(books_list_page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        books_tags = soup.select('table.d_book')

        for book_tag in books_tags:
            book_href = book_tag.select_one('.bookimage a')['href']
            book_url = urljoin(books_list_page_url, book_href)

            try:
                book_info = parse_book_page(book_url)

                if not args.skip_imgs:
                    book_info['img_src'] = download_image(
                        book_info['book_image'],
                        folder=os.path.join(args.dest_folder, 'images')
                    )

                if not args.skip_txt:
                    book_info['book_path'] = download_txt(
                        book_txt_url,
                        '{}. {}'.format(
                            book_info['book_id'],
                            book_info['book_title']
                        ),
                        folder=os.path.join(args.dest_folder, 'books'),
                        params={
                            'id': book_info['book_id']
                        },
                    )

                parsed_books.append(book_info)
            except requests.HTTPError:
                continue
    json_path = (
        args.json_path
        if args.json_path
        else os.path.join(args.dest_folder, 'results.json')
    )

    with open(json_path, 'w', encoding='utf-8') as books_json_file:
        json.dump(parsed_books, books_json_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
