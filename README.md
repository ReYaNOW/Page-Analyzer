### Hexlet tests and linter status:

[![Actions Status](https://github.com/ReYaNOW/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ReYaNOW/python-project-83/actions) [![Linter check](https://github.com/ReYaNOW/python-project-83/actions/workflows/action_tests.yml/badge.svg)](https://github.com/ReYaNOW/python-project-83/actions/workflows/action_tests.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/cabad60e2d465cd10b5f/maintainability)](https://codeclimate.com/github/ReYaNOW/python-project-83/maintainability)

Page Analyzer – это приложение, который анализирует указанные страницы на
SEO-пригодность.
При проверке веб-страницы при помощи Page Analyzer, приложение извлечет
несколько
HTML тегов важных для SEO.

![demo image](https://media.discordapp.net/attachments/324178393161793536/1195950731597983774/image.png)

# Использование

Открыть [тестовый вариант](https://page-analyzer-hexlet.onrender.com/)
задеплоенный на render.com

### Либо задеплоить приложение локально

Склонировать репозиторий

```
git clone https://github.com/ReYaNOW/python-project-83.git
```

Заполучить database url, например от запущенной так же локально БД

Создать файл .env в корневой директории проекта с примерно таким содержанием

```dotenv
DATABASE_URL=postgres://user:password@localhost:5432/dbname
SECRET_KEY=yoursecretkey
```  

Установить зависимости и добавить таблицы необходимые для работы приложения в
бд

```
make build
```

Запустить локальный сервер для разработки

```
make dev
```  
