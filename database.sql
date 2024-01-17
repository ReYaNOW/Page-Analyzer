CREATE TABLE IF NOT EXISTS urls
(
    id         serial PRIMARY KEY,
    name       varchar(255) NOT NULL UNIQUE,
    created_at date DEFAULT CURRENT_DATE
);


CREATE TABLE IF NOT EXISTS url_checks
(
    id          serial PRIMARY KEY,
    url_id      integer REFERENCES urls (id) ON DELETE CASCADE,
    status_code integer,
    h1          varchar(255),
    title       varchar(255),
    description varchar(255),
    created_at  date DEFAULT CURRENT_DATE
);