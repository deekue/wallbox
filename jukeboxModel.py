import sqlite3
import os

application_path = os.path.dirname(__file__)
dbFilePath = os.path.join(application_path, 'jukebox.db')

_conn = sqlite3.connect(dbFilePath, check_same_thread=False)
_conn.row_factory = sqlite3.Row
_cursor = _conn.cursor()

TRACKS_SCHEMA = """
CREATE TABLE IF NOT EXISTS tracks (
  id INTEGER PRIMARY KEY,
  wallbox INTEGER,
  letter TEXT,
  number INTEGER,
  artist TEXT,
  title TEXT,
  action INTEGER)
"""

def dict_from_row(row):
    return dict(zip(row.keys(), row))       

class JukeboxModel:
    def __init__(self):
        pass

    @classmethod
    def create_tables(self):
        _cursor.execute(TRACKS_SCHEMA)
        _conn.commit()

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
            'REPLACE INTO tracks (id, wallbox, letter, number, artist, title, action) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (track['id'], track['wallbox'], track['letter'], track['number'], track['artist'], track['title'], track['action']))
        _conn.commit()


