import sqlite3
import os

application_path = os.path.dirname(__file__)
dbFilePath = os.path.join(application_path, '..', 'jukebox.db')

SELECTION_LETTERS=("A","B","C","D","E","F","G","H","J","K","L","M","N","P","Q","R","S","T","U","V")
MAX_NUMBER=10

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

    NOTE: letters I and O are skipped

    :wallbox: which wallbox to generate tracks for
    :highest_letter: generate tracks for A to highest_letter
    :highest_number: generate tracks for 1 to highest_number
    :returns: dict(success=[True|False], tracks[(letter1, number1)...])

    """
    result = {}
    result['tracks'] = []

    # as far as I know, most wallboxes use 1-9,0
    if highest_number >= 10:
        number_range = range(1,10) + [0,]
    else:
        number_range = range(1,highest_number+1)

    try:
        highest_index=SELECTION_LETTERS.index(highest_letter)
    except ValueError:
        result['success'] = False
        return result

    for letter_index in range(0, highest_index+1):
        for number in number_range:
            result['tracks'].append((SELECTION_LETTERS[letter_index], number % highest_number))
            _cursor.execute(
                '''REPLACE INTO tracks (wallbox, letter, number, artist, title, action_title, action_cmd)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (wallbox, SELECTION_LETTERS[letter_index], number, '', '', '', '',))
    _conn.commit()
    result['success'] = True
    return result


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
            'SELECT * FROM tracks WHERE wallbox=? ORDER BY ID', (wallbox, )
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
            'REPLACE INTO tracks (ID, wallbox, letter, number, artist, title, action_title, action_cmd) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (track['ID'], track['wallbox'], track['letter'], track['number'], track['artist'], track['title'], track['action_title'], track['action_cmd']))
        _conn.commit()


