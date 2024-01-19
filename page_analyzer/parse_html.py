from bs4 import BeautifulSoup
from requests import Response


def get_specific_tags(response: Response):
    soup = BeautifulSoup(response.text, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    desc = soup.find('meta', attrs={'name': 'description'})

    return {
        'h1': h1.text[:255] if h1 else '',
        'title': title.text[:255] if title else '',
        'desc': desc.get('content', '') if desc else '',
    }
