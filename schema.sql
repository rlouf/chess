-- Schema for SQLITE3 database
BEGIN;

CREATE TABLE IF NOT EXISTS lichess (
    date TEXT NOT NULL,
    result TEXT NOT NULL,
    white TEXT,
    white_elo INT8,
    black TEXT,
    black_elo INT8,
    movetext TEXT NOT NULL
);

CREATE INDEX games_date ON lichess(date);
CREATE INDEX games_white ON lichess(white);
CREATE INDEX games_white_elo ON lichess(white_elo);
CREATE INDEX games_black ON lichess(black);
CREATE INDEX games_black_elo ON lichess(black_elo);

COMMIT;
