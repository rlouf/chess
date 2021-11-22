-- Schema for SQLITE3 database
BEGIN;

CREATE TABLE IF NOT EXISTS lichess (
    date TEXT NOT NULL,
    result TEXT NOT NULL,
    white_elo INT8,
    black_elo INT8,
    movetext TEXT NOT NULL
);

CREATE INDEX games_date ON lichess(date);
CREATE INDEX games_white_elo ON lichess(white_elo);
CREATE INDEX games_black_elo ON lichess(black_elo);

COMMIT;
