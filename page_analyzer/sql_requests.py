import os
from datetime import date

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor

load_dotenv('.env')
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

    def find_url_by_name(self, url):
        return self._make_request(
            'SELECT * FROM urls WHERE name=%s', [url], fetch_type='one'
        )

    def find_url_by_id(self, id_):
        return self._make_request(
            'SELECT * FROM urls WHERE id=%s', [id_], fetch_type='one'
        )

    def add_new_url(self, url):
        self._make_request(
            'INSERT INTO urls (name, created_at) VALUES (%s, %s)',
            [url, date.today()],
        )
        self.commit()
        added_url = self._make_request(
            'SELECT * FROM urls WHERE name=%s', [url], fetch_type='one'
        )
        return added_url.id

    def add_check(self, url_id):
        self._make_request(
            'INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s)',
            [url_id, date.today()],
        )

    def get_all_checks(self, url_id):
        return self._make_request(
            'SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC',
            [url_id],
            fetch_type='all',
        )

    def get_last_check(self, url_id):
        return self._make_request(
            'SELECT created_at FROM url_checks WHERE url_id=%s '
            'ORDER BY id DESC LIMIT 1',
            [url_id],
            fetch_type='one',
        )

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
