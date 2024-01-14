from bs4 import BeautifulSoup
from requests import Response


def get_specific_tags(response: Response):
    soup = BeautifulSoup(response.text, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    desc = soup.find('meta', attrs={'name': 'description'})

    return {
        'h1': '' if h1 is None else h1.text[:255],
        'title': '' if title is None else title.text[:255],
        'desc': '' if desc is None else desc.get('content', ''),
    }
