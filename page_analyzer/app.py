import secrets

from flask import (
    Flask,
    flash,
    url_for,
    request,
    redirect,
    render_template,
)
from requests.exceptions import RequestException

from page_analyzer.sql_requests import Database
from page_analyzer.utils import (
    validate_and_fix_url,
    make_http_request,
    get_specific_tags,
)

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    db = Database(connect=True)
    urls_with_code = db.get_urls_with_code()

    db.close()
    return render_template('url_related/urls.html', urls=urls_with_code)


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    db = Database(connect=True)
    url_info = db.get_url_by_id(id_=url_id)
    if not url_info:
        return render_template('url_related/url_not_found.html'), 404

    url_checks = db.get_all_checks_for_url(url_id)

    db.close()
    return render_template(
        'url_related/url.html', url=url_info, url_checks=url_checks
    )


@app.post('/urls')
def create_url_page():
    new_url = request.form.get('url')
    fixed_url = validate_and_fix_url(new_url)

    if not fixed_url:
        return render_template('index.html'), 422

    db = Database(connect=True)
    found_url = db.get_url_by_name(fixed_url)

    if not found_url:
        new_url_id = db.add_new_url(fixed_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', url_id=new_url_id))

    url_id = found_url.id
    flash('Страница уже существует', 'info')

    db.close()
    return redirect(url_for('get_url', url_id=url_id))


@app.post('/urls/<int:url_id>/checks')
def make_check(url_id):
    db = Database(connect=True)

    url = db.get_url_by_id(url_id).name
    try:
        request = make_http_request(url)
        tags = get_specific_tags(request.text)
        db.add_check(url_id, request.status_code, tags)
        db.commit()
        flash('Страница успешно проверена', 'success')

    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    db.close()
    return redirect(url_for('get_url', url_id=url_id))


@app.errorhandler(404)
def page_not_found(_):
    return render_template('url_related/url_not_found.html'), 404
