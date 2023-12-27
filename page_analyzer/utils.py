from urllib.parse import urlparse

import validators
from flask import flash


def validate_and_fix_url(url):
    if not url:
        flash('URL обязателен', 'danger')
        return False

    url = fix_url(url)
    if not validators.url(url):
        flash('Некорректный URL', 'danger')
        return False
    return True


def fix_url(url) -> str:
    parsed_url = urlparse(url)
    parsed_url = parsed_url._replace(query='')._replace(path='')  # noqa
    return str(parsed_url.geturl().lower())
