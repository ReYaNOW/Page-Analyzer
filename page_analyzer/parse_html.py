from bs4 import BeautifulSoup
from requests import Response


def get_specific_tags(response: Response):
    soup = BeautifulSoup(response.text, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    desc = soup.find('meta', attrs={'name': 'description'})

    return {
        'h1': get_content(h1),
        'title': get_content(title),
        'desc': get_content(desc),
    }


def get_content(tag):
    return '' if tag is None else tag.text[:255]
