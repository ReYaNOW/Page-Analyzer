PORT ?= 8000

install:
	poetry install

build:
	make install
	psql -a -d ${DATABASE_URL} -f database.sql

dev:
	poetry run flask --app page_analyzer:app --debug run --port 8000

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

truncate_db:
	psql -a -d ${DATABASE_URL} -c 'TRUNCATE TABLE urls, url_checks'