### Hexlet tests and linter status:

[![Actions Status](https://github.com/ReYaNOW/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ReYaNOW/python-project-83/actions) [![Linter check](https://github.com/ReYaNOW/python-project-83/actions/workflows/pyci.yml/badge.svg)](https://github.com/ReYaNOW/python-project-83/actions/workflows/action_tests.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/cabad60e2d465cd10b5f/maintainability)](https://codeclimate.com/github/ReYaNOW/python-project-83/maintainability)

Page Analyzer – это приложение, которое анализирует указанные страницы на
SEO-пригодность.
При проверке веб-страницы при помощи Page Analyzer приложение извлечет
несколько HTML тегов, важных для SEO.

![demo image](https://media.discordapp.net/attachments/324178393161793536/1195950731597983774/image.png)

# Использование

Открыть задеплоенный на render.com
[тестовый вариант](https://page-analyzer-hexlet.onrender.com/)

### Либо развернуть приложение локально

Склонировать репозиторий

```
git clone https://github.com/ReYaNOW/python-project-83.git
```

Развернуть БД PostgreSQL, как это сделать, можно
найти [тут](https://github.com/Hexlet/ru-instructions/blob/main/postgresql.md).
После этого составить database url.  
Ниже представлен формат такой ссылки.

```
postgresql://[user][:password]@[hostname][:port][/dbname]
```

Создать файл .env в корневой директории проекта примерно c таким содержанием

```dotenv
DATABASE_URL=postgres://user:password@localhost:5432/dbname
SECRET_KEY=yoursecretkey
```  

Установить зависимости и добавить таблицы в БД, необходимые для работы
приложения

```
make build
```

Запустить локальный сервер для разработки

```
make dev
```  

Либо задеплоить проект при помощи сервера gunicorn локально или например, на [render.com](https://render.com/)

```
make start
```  

### Минимальные требования:

- [Python^3.10](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [PostgreSQL](https://www.postgresql.org/)

#### Библиотеки Python:

- [Flask](https://pypi.org/project/Flask/)
- [Psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Gunicorn](https://pypi.org/project/gunicorn/)
- [Validators](https://pypi.org/project/validators/)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)

