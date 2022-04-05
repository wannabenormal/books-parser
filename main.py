import requests


def main():
    url = 'https://tululu.org/txt.php?id=32168'
    response = requests.post(url)
    response.raise_for_status()

    with open('mars.txt', 'wb') as book:
        book.write(response.content)


if __name__ == '__main__':
    main()
