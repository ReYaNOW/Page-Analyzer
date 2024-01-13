from urllib.parse import urlparse

import validators


def validate_url(url: str) -> str:
    if not url:
        return 'URL обязателен'

    if len(url) > 255:
        return 'URL превышает 255 символов'

    if not validators.url(url):
        return 'Некорректный URL'


def fix_url(url: str) -> str:
    parsed_url = urlparse(url)

    normalized_scheme = parsed_url.scheme.lower()
    normalized_host = parsed_url.hostname.lower()

    return f'{normalized_scheme}://{normalized_host}'
