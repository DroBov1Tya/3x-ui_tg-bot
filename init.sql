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
    ip          TEXT,
    user        TEXT,
    pass        TEXT,
    web_user    TEXT,
    web_pass    TEXT,
    web_path    TEXT,
    is_alive    boolean,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
)

CREATE TABLE configs (
    id          serial PRIMARY KEY,
    tg_user     TEXT,
    inbound     TEXT,
    user        TEXT,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
)


INSERT INTO users
    (id, tgid, nickname, is_banned, is_admin)
VALUES
    (1, 385922337, 'drobov1k', false, true),
    (2, 453533812, 'coder1', false, true),
    (3, 5123972512, 'alladon', false, true);
--