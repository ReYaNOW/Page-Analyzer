import secrets

from flask import (
    Flask,
    flash,
    url_for,
    request,
    redirect,
    get_flashed_messages,
    render_template,
)

from page_analyzer.sql_requests import Database
from page_analyzer.utils import validate_and_fix_url

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.get('/urls')
def get_urls():
    db = Database(connect=True)
    urls = db.get_all_urls()

    last_checks = {}
    for url in urls:
        lst_chck = db.get_last_check(url.id)
        last_checks[url.id] = lst_chck.created_at if lst_chck else ''
    db.close()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'url_related/urls.html',
        urls=urls,
        last_checks=last_checks,
        messages=messages,
    )


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    db = Database(connect=True)
    url_info = db.find_url_by_id(id_=url_id)
    if not url_info:
        return render_template('url_related/url_not_found.html'), 404

    url_checks = db.get_all_checks(url_id)

    db.close()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'url_related/url.html',
        url=url_info,
        url_checks=url_checks,
        messages=messages,
    )


@app.post('/urls')
def create_url_page():
    new_url = request.form.get('url')
    fixed_url = validate_and_fix_url(new_url)

    if not fixed_url:
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages)

    db = Database(connect=True)
    found_url = db.find_url_by_name(new_url)

    if not found_url:
        new_url_id = db.add_new_url(new_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', url_id=new_url_id), code=302)

    url_id = found_url.id
    flash('Страница уже существует', 'info')

    db.close()
    return redirect(url_for('get_url', url_id=url_id), code=302)


@app.post('/urls/<int:url_id>/checks')
def make_check(url_id):
    db = Database(connect=True)
    db.add_check(url_id)
    db.commit()

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', url_id=url_id), code=302)
