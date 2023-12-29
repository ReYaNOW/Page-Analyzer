from urllib.parse import urlparse

import validators
from flask import flash
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup


def validate_and_fix_url(url: str) -> str | bool:
    if not url:
        flash('URL обязателен', 'danger')
        return False

    url = fix_url(url)

    if len(url) > 255:
        flash('URL превышает 255 символов', 'danger')

    if not validators.url(url):
        flash('Некорректный URL', 'danger')
        return False
    return url


def fix_url(url: str) -> str:
    parsed_url = urlparse(url)

    normalized_scheme = parsed_url.scheme.lower()
    normalized_host = parsed_url.hostname.lower()

    return f'{normalized_scheme}://{normalized_host}'


def make_http_request(url: str) -> requests.Response:
    retries = Retry(
        total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504]
    )
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retries)

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) '
        'Gecko/20100101 Firefox/120.0'
    }
    response = session.get(url, timeout=0.5, headers=headers)
    return response


def get_specific_tags(page):
    soup = BeautifulSoup(page, 'html.parser')

    h1 = soup.find('h1')
    h1 = h1.string if h1 else None

    title = soup.title
    title = title.string if title else None

    tag = soup.head.find(attrs={'name': 'description'})
    desc = tag['content'] if tag else None

    return {'h1': h1, 'title': title, 'desc': desc}
