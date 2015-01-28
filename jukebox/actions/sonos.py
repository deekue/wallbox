#!/usr/bin/python


from yapsy.IPlugin import IPlugin

class Sonos(IPlugin):
    ACTIONS = ('play_uri', 'play_playlist')

    def play_uri(self, uri):
        return "playing %s" % uri

    def play_playlist(self, playlist):
        return "playing %s" % playlist


