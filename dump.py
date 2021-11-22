"""Dump the PGN files to sqlite3 database.

TODO:
    - Remove comments ?? ?! ! etc
    - When there is 1. 1... merge both to save space
"""
import datetime
import io
import re
import sqlite3
from typing import Iterator, Dict


HEADER_REGEX = re.compile("^\[([A-Za-z0-9_]+)\s+\"([^\r]*)\"\]\s*$")
EVAL_REGEX = re.compile("{ \[%eval .+?\] }")
CLOCK_REGEX = re.compile("{ \[%clk .+?\] }")

QUERY = """INSERT INTO lichess
           (date, result, white, white_elo, black, black_elo, movetext)
           VALUES (?, ?, ?, ?, ?, ?, ?)"""


def parse(handle: io.TextIOWrapper) -> Iterator[Dict]:
    """Parse a PGN file and return an iterator over the games.
    """

    parse_game = False
    parse_movetext = False
    line = handle.readline()
    while line:
        line = handle.readline()

        # start parsing game if it is a classical game.
        # we make the implicit assumption the first field in the game file in
        # 'Event'
        if 'Event' in line:
            if 'Classical game' in line:
                parse_game = True
                game = {}
                movetext=""
                continue

        if not parse_game:
            continue

        if parse_movetext:
            parse_movetext = False
            parse_game=False

            # We remove eol symbols and eval comments (mostly to save space)
            movetext = line.rstrip("\n")
            movetext = re.sub(EVAL_REGEX, '', movetext)
            game['movetext'] = movetext
            yield game

        if line.isspace():
            parse_movetext=True
            continue

        if 'UTCDate' in line:
            header = HEADER_REGEX.match(line)
            if header:
                game['date'] = datetime.datetime.strptime(header.group(2), "%Y.%m.%d").date()
                continue
            else:
                break
        elif 'WhiteElo' in line:
            header = HEADER_REGEX.match(line)
            if header:
                try:
                    game['white_elo'] = int(header.group(2))
                except ValueError:
                    game['white_elo'] = None
                continue
            else:
                break
        elif 'BlackElo' in line:
            header = HEADER_REGEX.match(line)
            if header:
                try:
                    game['black_elo'] = int(header.group(2))
                except ValueError:
                    game['black_elo'] = None

                continue
            else:
                game
                break
        elif 'White' in line:
            header = HEADER_REGEX.match(line)
            if header:
                try:
                    game['white'] = int(header.group(2))
                except ValueError:
                    game['white'] = None
                continue
            else:
                break
        elif 'Black' in line:
            header = HEADER_REGEX.match(line)
            if header:
                try:
                    game['black'] = int(header.group(2))
                except ValueError:
                    game['black'] = None
                continue
            else:
                break
        elif 'Result' in line:
            header = HEADER_REGEX.match(line)
            if header:
                game['result'] = header.group(2)
                continue
            else:
                break

if __name__ == "__main__":

    conn = sqlite3.connect('/archive/chess/lichess.db')

    with open('/archive/chess/lichess_db_standard_rated_2014-12.pgn', 'r') as handle:
        games = parse(handle)
        cur = conn.cursor()
        for game in games:
            cur.execute(QUERY, (game['date'], game['result'], game['white'], game['white_elo'], game['black'], game['black_elo'], game['movetext']))
        conn.commit()

