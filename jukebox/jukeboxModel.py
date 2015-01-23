import sqlite3
import os

application_path = os.path.dirname(__file__)
dbFilePath = os.path.join(application_path, '..', 'jukebox.db')

TRACKS_SCHEMA = """
CREATE TABLE IF NOT EXISTS tracks (
  ID      INTEGER PRIMARY KEY AUTOINCREMENT,
  wallbox INTEGER NOT NULL,
  letter  TEXT NOT NULL,
  number  INTEGER NOT NULL,
  artist  TEXT NOT NULL,
  title   TEXT NOT NULL,
  action_title  TEXT NOT NULL,
  action_cmd    TEXT NOT NULL,
  UNIQUE(wallbox, letter, number)
);
"""

SETTINGS_SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
  ID       INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL,
  key      TEXT NOT NULL,
  value    TEXT NOT NULL,
  UNIQUE(category, key)
);
"""

_conn = sqlite3.connect(dbFilePath, check_same_thread=False)
_conn.row_factory = sqlite3.Row
_cursor = _conn.cursor()

# create tables
_cursor.execute(TRACKS_SCHEMA)
_conn.commit()
_cursor.execute(SETTINGS_SCHEMA)
_conn.commit()

def dict_from_row(row):
    return dict(zip(row.keys(), row))       

def generate_tracks(wallbox, highest_letter='V', highest_number=10):
    """generate tracks for a wallox for the specified max letter/number
    this will overwrite any existing tracks for the specified wallbox

    :wallbox: which wallbox to generate tracks for
    :highest_letter: generate tracks for A to highest_letter
    :highest_number: generate tracks for 1 to highest_number
    :returns: None

    """
    # as far as I know, most wallboxes use 1-9,0
    if highest_number > 10:
        highest_number = 10
    for letter in range(ord('A'), ord(highest_letter)):
        for number in range(1, highest_number+1):
            print "%d %s%d" % (wallbox, chr(letter), number % 10)
            _cursor.execute(
                '''REPLACE INTO tracks (wallbox, letter, number, artist, title, action_title, action_cmd)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (wallbox, chr(letter), number % 10, '', '', '', '',))
    _conn.commit()


class JukeboxModel:
    def __init__(self):
        pass

    @classmethod
    def retrieve_tracks(self, wallbox):
        """retrieve list of tracks for specified wallbox

        :wallbox: wallbox number to retrieve tracks for
        :returns: list of tracks

        """
        rows = _cursor.execute(
            'SELECT * FROM tracks WHERE wallbox=?', (wallbox, )
        )
        return [dict_from_row(item) for item in rows.fetchall()]
        

    @classmethod
    def retrieve_track(cls, wallbox, letter, number):
        rows = _cursor.execute(
            'SELECT * FROM tracks WHERE wallbox=? AND letter=? AND number=?',
            (wallbox, letter, number, )
        )
        return rows.fetchone()

    @classmethod
    def update_track(self, track):
        """update specified track information, create if missing.

        :track: dict of track data
        :returns: None

        """
        _cursor.execute(
            'REPLACE INTO tracks (ID, wallbox, letter, number, artist, title, action) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (track['id'], track['wallbox'], track['letter'], track['number'], track['artist'], track['title'], track['action']))
        _conn.commit()

