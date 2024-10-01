/*============================[Xui bớt DATABASE MODEL]============================| */

CREATE TABLE users (
    id              serial PRIMARY KEY,
    tgid            BIGINT NOT NULL UNIQUE,
    nickname        TEXT,
    first_name      TEXT,
    last_name       TEXT,
    balance         INT DEFAULT 0,
    user_level      SMALLINT DEFAULT 0, /* 0 - demo, 1 - basic, 2 - advanced, 3 - premium */
    is_banned       boolean NOT NULL DEFAULT true,
    is_admin        boolean NOT NULL DEFAULT false,
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
    ttl         TIMESTAMP DEFAULT NOW(), /*BIGINT*/
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE configs_history (
    id          serial PRIMARY KEY,
    hostname    TEXT,
    tg_user     TEXT,
    inbound     TEXT,
    users       TEXT,
    config      TEXT,
    ttl         TIMESTAMP DEFAULT NOW(),     /*BIGINT*/
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);


INSERT INTO users
    (id, tgid, nickname, is_banned, is_admin)
VALUES
    (1, 385922337, 'drobov1k', false, true),
    (2, 453533812, 'coder1', false, true),
    (3, 5123972512, 'alladon', false, true);
