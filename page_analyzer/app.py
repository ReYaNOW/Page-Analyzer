from urllib.parse import urlparse

from flask import (
    Flask,
    flash,
    url_for,
    request,
    redirect,
    get_flashed_messages,
    render_template,
)
import validators
import secrets

from page_analyzer.sql_requests import get_all_urls, find_url, add_new_url

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


def validate_url(url):
    if not url:
        flash('URL обязателен', 'danger')
        return False
    if not validators.url(url):
        flash('Некорректный URL', 'danger')
        return False
    return True


def fix_url(url):
    parsed_url = urlparse(url)
    parsed_url = parsed_url._replace(query='')._replace(path='')  # noqa
    return parsed_url.geturl().lower()


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.get('/urls')
def get_urls():
    messages = get_flashed_messages(with_categories=True)
    urls = get_all_urls(desc_order=True)
    return render_template(
        'url_related/urls.html', urls=urls, messages=messages
    )


@app.post('/urls')
def create_url_page():
    new_url = request.form.get('url')
    new_url = fix_url(new_url)

    if not validate_url(new_url):
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages)

    found_url = find_url(new_url)
    if not found_url:
        new_url_id = add_new_url(new_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', url_id=new_url_id))

    url_id = found_url.id
    flash('Страница уже существует', 'info')
    return redirect(url_for('get_url', url_id=url_id))


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    messages = get_flashed_messages(with_categories=True)
    url_info = find_url(id_=url_id)
    return render_template(
        'url_related/url.html', url=url_info, messages=messages
    )
