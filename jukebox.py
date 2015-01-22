#!/usr/bin/python

# jukebox use cases
# - background music playing (playlist)
#   - new selection plays after current song then playlist continues
#     - each new selection is added *after* the previous selection but before
#     the rest of the playlist
# - no current music
#   - new selection added to queue, plays immediately
#     - each new selection is added to end of queue
# - statically configured speaker
#   - if speaker is part of a group, play to the group
#     - add to that playlist
#   - if speaker is a singleton, play to just that speaker
#   - option for 'partymode'
#     - group all speakers, take over playlist
#
# - actions
#   - Sonos play_uri
#   - Youtube via Chromecast?
#   - Local play (hook speakers to RPi)
#   - System command
#
# - webui
#   - software
#      - angular+bootstrap client
#      - flask as backend (pip install flask)
#      - sqlite as db
#   - track configuration page
#      - paginated, 10 per page (to match jukebox)
#      - configure action for each selection
#        - single song
#        - playlist
#        - radio station
#        - partymode
#        - run external command
#   - settings page
#      - set wallbox type (sets number of tracks)
#         - pick from templates or manual setup
#      - select Sonos unit to pair with
#      - counters?
#   - print track labels?

# CRUD api
# /api/play/<wallbox>/<letter>/<number>
#   GET - play selected entry
# /api/tracks/<wallbox>
#   GET - get list of tracks (just artist - title)
# /api/track/<wallbox>/<letter>/<number>
#   GET  - get track info (artist, title, action)
#   POST - update track info
# /api/settings
#   GET - retrieve settings
# /api/setting/<category>
#   GET - retrieve specified category from settings
#   POST - update settings in category, create if blank
# /api/setting/<category>/<item>
#   GET - retrieve specified item from specified category
#   POST - update specified setting in specified category

# DB schema
# tracks
#   id - int primary key
#   wallbox - int
#   letter - text
#   number - int
#   artist - text
#   title  - text
#   action - int
# settings
#   id - int primary key
#   category - text
#   item - text
#   value - text

from flask import Flask

from jukebox.jukeboxView import JukeboxView, JukeboxPlay, JukeboxTrack, JukeboxTracks

app = Flask(__name__)

app.add_url_rule('/', view_func=JukeboxView.as_view('jukebox_view'),
    methods=['GET'])
app.add_url_rule('/api/play/<int:wallbox>/<letter>/<int:number>',
        view_func=JukeboxPlay.as_view('jukebox_play'))
app.add_url_rule('/api/tracks/<int:wallbox>',
        view_func=JukeboxTracks.as_view('jukebox_tracks'), methods=['GET'])
app.add_url_rule('/api/track/<int:wallbox>/<letter>/<int:number>',
        view_func=JukeboxTrack.as_view('jukebox_track'), methods=['GET',
            'POST',])
# TODO add routing for settings

if __name__ == '__main__':
    app.run(debug=True)
