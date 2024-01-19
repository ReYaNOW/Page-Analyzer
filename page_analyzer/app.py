import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    url_for,
    request,
    redirect,
    render_template,
    abort,
)

from page_analyzer.db import DbConnectionProcessor
from page_analyzer.parse_html import get_specific_tags
from page_analyzer.utils import validate_url, normalize_url

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def show_urls():
    db = DbConnectionProcessor()
    urls_with_code = db.get_urls_with_code()

    db.close()
    return render_template('urls/urls.html', urls=urls_with_code)


@app.route('/urls/<int:url_id>')
def show_url_page(url_id):
    db = DbConnectionProcessor()
    url_info = db.get_url_by_id(id_=url_id)
    if not url_info:
        return abort(404)

    url_checks = db.get_all_checks_for_url(url_id)

    db.close()
    return render_template(
        'urls/url.html', url=url_info, url_checks=url_checks
    )


@app.post('/urls')
def create_url_page():
    url = request.form.get('url')
    error_message = validate_url(url)

    if error_message:
        flash(error_message, 'danger')
        return render_template('index.html'), 422

    fixed_url = normalize_url(url)
    db = DbConnectionProcessor()
    found_url = db.get_url_by_name(fixed_url)

    if found_url:
        flash('Страница уже существует', 'info')
        new_url_id = found_url.id
    else:
        new_url_id = db.add_new_url(fixed_url)
        flash('Страница успешно добавлена', 'success')

    db.close()
    return redirect(url_for('show_url_page', url_id=new_url_id))


@app.post('/urls/<int:url_id>/checks')
def process_url_check(url_id):
    db = DbConnectionProcessor()
    url = db.get_url_by_id(url_id)

    try:
        resp = requests.get(url.name)
        resp.raise_for_status()
    except requests.RequestException:
        db.close()
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url_page', url_id=url_id))

    tags = get_specific_tags(resp)
    db.add_check(url_id, resp.status_code, tags)
    db.close()
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url_page', url_id=url_id))


@app.errorhandler(404)
def page_not_found(_):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(_):
    return render_template('errors/500.html'), 500
