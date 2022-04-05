from pathlib import Path

import requests


def check_for_redirect(response):
    if response.status_code >= 300 and response.status_code < 400:
        raise requests.HTTPError


def main():
    Path("./books").mkdir(parents=True, exist_ok=True)

    for book_id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={book_id}'
        response = requests.post(url, allow_redirects=False)
        response.raise_for_status()

        try:
            check_for_redirect(response)
        except requests.HTTPError:
            continue

        with open(f'./books/id{book_id}.txt', 'wb') as book:
            book.write(response.content)


if __name__ == '__main__':
    main()
