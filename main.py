from pathlib import Path

import requests


def main():
    Path("./books").mkdir(parents=True, exist_ok=True)

    for book_id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={book_id}'
        response = requests.post(url)
        response.raise_for_status()

        with open(f'./books/id{book_id}.txt', 'wb') as book:
            book.write(response.content)


if __name__ == '__main__':
    main()
