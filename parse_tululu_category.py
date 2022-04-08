import argparse
import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from main import parse_book_page, download_txt, download_image


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
        type=int, default=10,
        help='По какую страницу парсить'
    )
    args = parser.parse_args()

    category_page_url_template = 'https://tululu.org/l55/{}/'
    book_txt_url = 'https://tululu.org/txt.php'
    parsed_books = []

    for page_number in range(args.start_page, args.end_page + 1):
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
                book_image_path = download_image(book_info['book_image'])
                book_txt_path = download_txt(
                    book_txt_url,
                    '{}. {}'.format(
                        book_info['book_id'],
                        book_info['book_title']
                    ),
                    params={
                        'id': book_info['book_id']
                    }
                )

                parsed_books.append(
                    {
                        'title': book_info['book_title'],
                        'author': book_info['book_author'],
                        'img_src': book_image_path,
                        'book_path': book_txt_path,
                        'comments': book_info['comments'],
                        'genres': book_info['genres']
                    }
                )
            except requests.HTTPError:
                continue

    with open('books.json', 'w', encoding='utf-8') as books_json_file:
        json.dump(parsed_books, books_json_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
