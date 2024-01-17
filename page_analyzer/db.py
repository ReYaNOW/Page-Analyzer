import os
from collections import namedtuple

import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

_FETCH_TYPE_VALUES = ('one', 'all')
FETCH_TYPES = namedtuple('FormatChoices', map(str.upper, _FETCH_TYPE_VALUES))(
    *_FETCH_TYPE_VALUES
)


class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)

    def _execute_query(self, request, params=None, fetch_type=None):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(request, params)

            match fetch_type:
                case FETCH_TYPES.ALL:
                    return curs.fetchall()
                case FETCH_TYPES.ONE:
                    return curs.fetchone()
                case _:
                    return []

    def _execute_query_with_fetch(self, request, params=None, fetch_type=None):
        pass

    def get_all_urls(self):
        return self._execute_query(
            'SELECT * FROM urls ORDER BY id DESC', fetch_type='all'
        )

    def get_url_by_name(self, url):
        return self._execute_query(
            'SELECT * FROM urls WHERE name=%s', (url,), fetch_type='one'
        )

    def get_url_by_id(self, id_):
        return self._execute_query(
            'SELECT * FROM urls WHERE id=%s', (id_,), fetch_type='one'
        )

    def add_new_url(self, url):
        added_url = self._execute_query(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id',
            (url,),
            fetch_type='one',
        )
        self.conn.commit()
        return added_url.id

    def add_check(self, url_id, status_code, tags):
        h1, title, desc = tags['h1'], tags['title'], tags['desc']
        self._execute_query(
            'INSERT INTO url_checks '
            '(url_id, status_code, h1, title, description) '
            'VALUES (%s, %s, %s, %s, %s)',
            (url_id, status_code, h1, title, desc),
        )
        self.conn.commit()

    def get_all_checks_for_url(self, url_id):
        return self._execute_query(
            'SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC',
            (url_id,),
            fetch_type='all',
        )

    def get_urls_with_code(self):
        return self._execute_query(
            'SELECT DISTINCT ON (urls.id) urls.id, name,  '
            'url_checks.created_at AS last_check, '
            'status_code AS last_code '
            'FROM urls '
            'LEFT JOIN url_checks ON urls.id = url_checks.url_id '
            'ORDER BY urls.id DESC',
            fetch_type='all',
        )

    def close(self):
        self.conn.close()
