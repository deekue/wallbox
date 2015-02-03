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
            (res, msg) = self.setDefaultPlayer('Kitchen')
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
            state = self._defaultPlayer.group.coordinator.get_current_transport_info()
            if state['current_transport_state'] != "PLAYING":
                # this is racy but it's a music player not a nuclear power plant
                q = self._defaultPlayer.get_queue()
                self._defaultPlayer.play_from_queue(len(q)-1)
            return "queueing %s" % uri
        else:
            return "no default player set"

    def play_playlist(self, playlist):
        # TODO enqueue each item in the playlist?  or just let Sonos handle it?
        return self.play_uri(playlist)

    def setDefaultPlayer(self, playerName):
        if self._players.has_key(playerName):
            self._defaultPlayer = self._players[playerName]
            return (True, "default player set to %s" % playerName)
        else:
            return (False, "player %s not found" % playerName)

    def refreshPlayerList(self):
        players = soco.discover()
        for player in players:
            self._players[player.player_name] = player



