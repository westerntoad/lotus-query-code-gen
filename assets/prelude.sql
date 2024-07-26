/*********************************
 Project Phase II
 Group Lotus Query
 This SQL Script was tested on MySQL Workbench. To run, simply load this script
 file and run.
**********************************/

-- generic note: the expected order of colors in attributes/tables, unless
-- otherwise specified is determined by the following order:
-- white (w) -> blue (u) -> black (b) -> red (r) -> green (g)

/****************
PART A
****************/

CREATE TABLE IF NOT EXISTS sets (
    set_id            VARCHAR(6),
    set_name          VARCHAR(60)             NOT NULL,
    release_date      DATE,

    CHECK(release_date >= '1993-08-05'),

    PRIMARY KEY (set_id)
);

CREATE TABLE IF NOT EXISTS cmc (
    mana_cost VARCHAR(50),
    cmc       MEDIUMINT UNSIGNED      NOT NULL,

    CHECK((
        mana_cost LIKE '{%}' AND
        mana_cost LIKE '%{%}%'
    ) OR mana_cost = ''),

    PRIMARY KEY (mana_cost)
);

CREATE TABLE IF NOT EXISTS color (
    abbr      VARCHAR(5),
    white     BOOLEAN         NOT NULL,
    blue      BOOLEAN         NOT NULL,
    black     BOOLEAN         NOT NULL,
    red       BOOLEAN         NOT NULL,
    green     BOOLEAN         NOT NULL,

    CHECK( abbr = '' OR NOT (
        abbr NOT LIKE '%W%' AND
        abbr NOT LIKE '%U%' AND
        abbr NOT LIKE '%B%' AND
        abbr NOT LIKE '%R%' AND
        abbr NOT LIKE '%G%'
    )),

    PRIMARY KEY (abbr)
);

CREATE TABLE IF NOT EXISTS cards (
    -- "uuid" property in json
    uuid              CHAR(36),
    -- id of the set (3-6 letters on bottom left of card)
    set_id            VARCHAR(6)      NOT NULL,
    name              VARCHAR(141)    NOT NULL DEFAULT '',
    type              VARCHAR(16)     NOT NULL,
    mana_cost         VARCHAR(50)     NOT NULL DEFAULT '',
    -- WUBRG (colors in the cost) ->
    color             VARCHAR(5),
    -- WUBRG (colors in text, ..., and cost) ->
    color_identity    VARCHAR(5),
    rarity			  ENUM('common', 'uncommon', 'rare', 'mythic', 'special', 'bonus'),
    
    PRIMARY KEY (uuid),
    FOREIGN KEY (set_id)                REFERENCES sets(set_id)         ON DELETE CASCADE,
    FOREIGN KEY (mana_cost)             REFERENCES cmc(mana_cost)		ON DELETE RESTRICT,
    FOREIGN KEY (color)                 REFERENCES color(abbr)			ON DELETE RESTRICT,
    FOREIGN KEY (color_identity)        REFERENCES color(abbr)
);

CREATE TABLE IF NOT EXISTS creature (
    -- "uuid" property in json
    -- child of 'cards' table
    uuid      CHAR(36),
    power     VARCHAR(8)                NOT NULL,
    toughness VARCHAR(8)                NOT NULL,

	-- needs fixing
    -- CHECK( power 	 REGEXP '^[0-9+*]+$' OR power = '*' ),
    -- CHECK( toughness REGEXP '^[0-9+*]+$' OR toughness = '*'),

    PRIMARY KEY (uuid),
    FOREIGN KEY (uuid)  REFERENCES cards(uuid)
);

CREATE TABLE IF NOT EXISTS legality (
    -- "uuid" property in json
    -- child of 'cards' table
    uuid              CHAR(36),
    commander         ENUM('legal', 'banned')                 NOT NULL DEFAULT 'banned',
    legacy            ENUM('legal', 'banned')                 NOT NULL DEFAULT 'banned',
    modern            ENUM('legal', 'banned')                 NOT NULL DEFAULT 'banned',
    pauper            ENUM('legal', 'banned')                 NOT NULL DEFAULT 'banned',
    pioneer           ENUM('legal', 'banned')                 NOT NULL DEFAULT 'banned',
    standard          ENUM('legal', 'banned')                 NOT NULL DEFAULT 'banned',
    vintage           ENUM('legal', 'restricted', 'banned')   NOT NULL DEFAULT 'banned',

    PRIMARY KEY (uuid),
    FOREIGN KEY (uuid)  REFERENCES cards(uuid)
);

/****************
PART B
****************/

--           ~ PRELUDE ~
-- (not programmatically generated)
--           ~ PRELUDE ~
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WUBRG', TRUE, TRUE, TRUE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WBRG', TRUE, FALSE, TRUE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WURG', TRUE, TRUE, FALSE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('UBRG', FALSE, TRUE, TRUE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WUBG', TRUE, TRUE, TRUE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WUBR', TRUE, TRUE, TRUE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('BRG', FALSE, FALSE, TRUE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('UBR', FALSE, TRUE, TRUE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WRG', TRUE, FALSE, FALSE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WUR', TRUE, TRUE, FALSE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WUB', TRUE, TRUE, TRUE, FALSE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WBR', TRUE, FALSE, TRUE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WBG', TRUE, FALSE, TRUE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('UBG', FALSE, TRUE, TRUE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('URG', FALSE, TRUE, FALSE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WUG', TRUE, TRUE, FALSE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WB', TRUE, FALSE, TRUE, FALSE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('UR', FALSE, TRUE, FALSE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WU', TRUE, TRUE, FALSE, FALSE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WG', TRUE, FALSE, FALSE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('BR', FALSE, FALSE, TRUE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('UB', FALSE, TRUE, TRUE, FALSE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('RG', FALSE, FALSE, FALSE, TRUE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('BG', FALSE, FALSE, TRUE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('UG', FALSE, TRUE, FALSE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('WR', TRUE, FALSE, FALSE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('B', FALSE, FALSE, TRUE, FALSE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('G', FALSE, FALSE, FALSE, FALSE, TRUE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('W', TRUE, FALSE, FALSE, FALSE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('U', FALSE, TRUE, FALSE, FALSE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('R', FALSE, FALSE, FALSE, TRUE, FALSE);
INSERT INTO color (abbr, white, blue, black, red, green) VALUES ('', FALSE, FALSE, FALSE, FALSE, FALSE);

INSERT IGNORE INTO cmc (mana_cost, cmc) VALUES ('', 0);

--        ~ END PRELUDE ~
-- (not programmatically generated
--        ~  END PRELUDE ~
