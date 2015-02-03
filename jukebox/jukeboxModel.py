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
  action_plugin  TEXT NOT NULL,
  action_args    TEXT NOT NULL,
  UNIQUE(wallbox, letter, number)
);
"""

SETTINGS_SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
  ID       INTEGER PRIMARY KEY AUTOINCREMENT,
  section  TEXT NOT NULL,
  option   TEXT NOT NULL,
  value    TEXT NOT NULL,
  UNIQUE(section, option)
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
            'REPLACE INTO tracks (ID, wallbox, letter, number, artist, title, action_plugin, action_args) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (track['ID'], track['wallbox'], track['letter'], track['number'], track['artist'], track['title'], track['action_plugin'], track['action_args']))
        _conn.commit()

    @classmethod
    def generate_empty_tracks(self, highest_letter='V', highest_number=10):
        """generate tracks for a wallox for the specified max letter/number
        this will overwrite any existing tracks for the specified wallbox

        NOTE: letters I and O are skipped

        :highest_letter: generate tracks for A to highest_letter
        :highest_number: generate tracks for 1 to highest_number
        """
        # as far as I know, most wallboxes use 1-9,0
        if highest_number >= 10:
            number_range = range(1,10) + [0,]
        else:
            number_range = range(1,highest_number+1)

        try:
            highest_index=SELECTION_LETTERS.index(highest_letter)
        except ValueError:
            highest_index=len(SELECTION_LETTERS)-1

        for letter_index in range(0, highest_index+1):
            for number in number_range:
                yield {'letter': SELECTION_LETTERS[letter_index], 'number': number,
                    'artist': '', 'title': '', 'action_plugin': '', 'action_args': ''}

    @classmethod
    def generate_static_sonos_tracks(self, highest_letter, highest_number):
        """TODO this should be part of the Sonos plugin"""
        for track in JukeboxModel.generate_empty_tracks(highest_letter,
                highest_number):
            track['action_plugin'] = 'SONOS.play_file'
            track['action_args'] = '%s%s.mp3' % (track['letter'], track['number'])
            yield track

    @classmethod
    def set_tracks(self, wallbox, track_generator):
        """create tracks in the db for the given wallbox using the specified
        generator for input.

        :param wallbox: id of the wallbox to generate tracks for
        :type wallbox: int
        :param track_generator: a Python generator that a dict for each track of the form
            {'letter': 'A', 'number': 1, 'artist': 'Elvis Parsely', 'title': 'Heart
            Break Motel', 'action_plugin': 'SONOS.play_file', 'action_args':
            'A1.mp3'}
            letter and nubmer are required, everything else is optional
        """
        result = {}
        with _conn:
            for item in track_generator:
                track = '%s%s' % (item['letter'], item['number'])
                result[track] = (wallbox, item['letter'], item['number'], item['artist'],
                       item['title'], item['action_plugin'], item['action_args'])
                _cursor.execute(
                    '''REPLACE INTO tracks (wallbox, letter, number, artist, title, action_plugin, action_args)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    result[track])
        return result

