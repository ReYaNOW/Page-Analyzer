import os
from datetime import date

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor

load_dotenv(r'C:\Users\ReYaN\python_projects\python-project-83\.env')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_all_urls(desc_order=False):
    conn = psycopg2.connect(DATABASE_URL)
    desc_str = 'DESC' if desc_order else ''

    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(f'SELECT * FROM urls ORDER BY id {desc_str}')
        found_url = curs.fetchall()

    conn.commit()
    conn.close()
    return found_url


def find_url(url=None, id_=None):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        if url:
            curs.execute(f'SELECT * FROM urls WHERE name=%s', [url])
        else:
            curs.execute(f'SELECT * FROM urls WHERE id=%s', [id_])
        found_url = curs.fetchone()

    conn.commit()
    conn.close()
    return found_url


def add_new_url(url):
    conn = psycopg2.connect(DATABASE_URL)
    current_date = date.today()

    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'INSERT INTO urls (name, created_at) VALUES (%s, %s)',
            [url, current_date],
        )
        curs.execute(f'SELECT * FROM urls WHERE name=%s', [url])
        found_url = curs.fetchone()

    conn.commit()
    conn.close()
    return found_url.id
