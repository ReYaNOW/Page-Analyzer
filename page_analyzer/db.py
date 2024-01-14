import os

import psycopg2
from psycopg2.extras import NamedTupleCursor

DATABASE_URL = os.getenv('DATABASE_URL')


class Database:
    def __init__(self, connect=False):
        if connect:
            self.conn = psycopg2.connect(DATABASE_URL)
        else:
            self.conn = None

    def _make_request(self, request, params=None, fetch_type=None):
        if self.conn is None:
            raise ConnectionError(
                'Need to connect to db before making requests'
            )

        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(request, params)

            match fetch_type:
                case 'all':
                    data = curs.fetchall()
                case 'one':
                    data = curs.fetchone()
                case _:
                    data = None
        return data

    def get_all_urls(self):
        return self._make_request(
            'SELECT * FROM urls ORDER BY id DESC', fetch_type='all'
        )

    def get_url_by_name(self, url):
        return self._make_request(
            'SELECT * FROM urls WHERE name=%s', [url], fetch_type='one'
        )

    def get_url_by_id(self, id_):
        return self._make_request(
            'SELECT * FROM urls WHERE id=%s', [id_], fetch_type='one'
        )

    def add_new_url(self, url):
        self._make_request(
            'INSERT INTO urls (name) VALUES (%s)',
            [url],
        )
        self.commit()
        added_url = self._make_request(
            'SELECT * FROM urls WHERE name=%s', [url], fetch_type='one'
        )
        return added_url.id

    def add_check(self, url_id, status_code, tags):
        h1, title, desc = tags['h1'], tags['title'], tags['desc']
        self._make_request(
            'INSERT INTO url_checks '
            '(url_id, status_code, h1, title, description) '
            'VALUES (%s, %s, %s, %s, %s)',
            [url_id, status_code, h1, title, desc],
        )

    def get_all_checks_for_url(self, url_id):
        return self._make_request(
            'SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC',
            [url_id],
            fetch_type='all',
        )

    def get_urls_with_code(self):
        return self._make_request(
            'SELECT DISTINCT ON (urls.id) urls.id, name,  '
            'url_checks.created_at AS last_check, '
            'status_code AS last_code '
            'FROM urls '
            'LEFT JOIN url_checks ON urls.id = url_checks.url_id '
            'ORDER BY urls.id DESC',
            fetch_type='all',
        )

    def connect(self):
        self.conn = psycopg2.connect(DATABASE_URL)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
