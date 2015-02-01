#!/usr/bin/python

import os
from yapsy.IPlugin import IPlugin
try:
    import soco
except ImportError:
    soco = None

class Sonos(IPlugin):
    ACTIONS = ('play_file', 'play_uri', 'play_playlist')
    _players = {}
    _defaultPlayer = None

    def activate(self):
        if soco is None:
            return False
        else:
            self.refreshPlayerList()
            # TODO get default player from settings
            print 'setting default player to Kitchen'
            (res, msg) = self.setDefaultPlayer('Kitchen')
            print msg
            if res:
                super(Sonos, self).activate()

    def play_file(self, filename):
        # TODO add plugin setting for host/path
        host = 'nyx'
        path = 'music/jukebox'
        uri = os.path.join('x-file-cifs://', host, path, filename)
        return self.play_uri(uri)

    def play_uri(self, uri):
        if self._defaultPlayer is not None:
            self._defaultPlayer.add_uri_to_queue(uri)
            self._defaultPlayer.play()
            return "playing %s" % uri
        else:
            return "no default player set"

    def play_playlist(self, playlist):
        if self._defaultPlayer is not None:
            return "playing %s" % playlist
        else:
            return "no default player set"

    def setDefaultPlayer(self, playerName):
        # TODO fix this
        self._defaultPlayer = soco.SoCo("192.168.136.112")
        if self._players.has_key(playerName):
            self._defaultPlayer = self._players[playerName]
            return (True, "default player set to %s" % playerName)
        else:
            return (False, "player %s not found" % playerName)

    def refreshPlayerList(self):
        players = soco.discover()
        print players
        for player in self._players:
            print 'adding player %s' % player.player_name
            self._players[player.player_name] = player



