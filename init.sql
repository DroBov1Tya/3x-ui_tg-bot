/*============================[Xui bớt DATABASE MODEL]============================| */

CREATE TABLE users (
    id              serial PRIMARY KEY,
    tgid            BIGINT NOT NULL UNIQUE,
    tg_user         TEXT,
    first_name      TEXT,
    last_name       TEXT,
    config_limit    SMALLINT NOT NULL,
    is_banned       boolean NOT NULL DEFAULT true,
    is_admin        boolean NOT NULL DEFAULT false,
    sub             BIGINT, /* Unix time для окончания подписки */
    lang            TEXT NOT NULL DEFAULT 'en',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE servers (
    id          serial PRIMARY KEY,
    hostname    TEXT,
    port        TEXT,
    username    TEXT,
    passwd      TEXT,
    country     TEXT,
    web_user    TEXT,
    web_pass    TEXT,
    web_path    TEXT,
    is_alive    boolean,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE configs (
    id          serial PRIMARY KEY,
    hostname    TEXT,
    tg_user     TEXT,
    inbound     TEXT,
    users       TEXT,
    config      TEXT,
    ttl         BIGINT, 
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE configs_history (
    id          serial PRIMARY KEY,
    hostname    TEXT,
    tg_user     TEXT,
    inbound     TEXT,
    users       TEXT,
    config      TEXT,
    ttl         BIGINT,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE vouchers (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(50) NOT NULL UNIQUE, -- Уникальный код ваучера
    discount_type   VARCHAR(20) NOT NULL, -- Например, 'subscription' для подписки
    duration        BIGINT NOT NULL, -- Количество месяцев для подписки
    is_used         BOOLEAN NOT NULL, -- Флаг, указывающий, использован ли ваучер
    created_at      BIGINT,
    expires_at      BIGINT -- Дата окончания действия ваучера
);

CREATE TABLE invoices (
    id                      SERIAL PRIMARY KEY,
    tgid                    INT,
    invoice_id              INT,
    invoice_hash            TEXT,
    currency_type           TEXT,
    asset                   TEXT,
    amount                  TEXT,
    invoice_description     TEXT,
    invoice_status          TEXT,
    created_at              TEXT,
    expiration_date         TEXT
);

