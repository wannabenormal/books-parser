import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1', class_='entry-title').text
    img = soup.find('img', class_='attachment-post-image')
    post_body = soup.find('div', class_='entry-content')
    print(title)
    print(img['src'])
    print(post_body.text.strip())


if __name__ == '__main__':
    main()
