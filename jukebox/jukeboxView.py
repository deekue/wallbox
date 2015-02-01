from flask import request, jsonify, render_template
from jukeboxModel import JukeboxModel

import actions
import flask.views
import json


class JukeboxView(flask.views.MethodView):
    def get(self):
        return render_template('index.html')

class JukeboxPlay(flask.views.MethodView):
    def get(self, wallbox, letter, number):
        track = JukeboxModel.retrieve_track(wallbox, letter, number)
        (result, message) = actions.runAction(track['action_title'], track['action_cmd'])
        if result:
            message = "play track %s%s for wallbox %s via '%s %s': %s" % (letter,
                    number, wallbox, track['action_title'],
                    track['action_cmd'], message)
        return jsonify(result=result, message=message)

class JukeboxTracks(flask.views.MethodView):
    def get(self, wallbox):
        trackList = JukeboxModel.retrieve_tracks(wallbox)
        return json.dumps(trackList)

class JukeboxTrack(flask.views.MethodView):
    def get(self, wallbox, letter, number):
        track = JukeboxModel.retrieve_track(wallbox, letter, number)
        return jsonify(track)

    def post(self, wallbox, letter, number):
        track = json.loads(request.data)
        JukeboxModel.update_track(track)
        return jsonify(success=True)
        
class JukeboxGenTracks(flask.views.MethodView):
    # TODO this should be a POST
    # TODO should be using a specifed track generator (from plugins)
    def get(self, wallbox, highest_letter, highest_number):
        return jsonify(JukeboxModel.set_tracks(wallbox,
            JukeboxModel.generate_static_sonos_tracks(highest_letter, highest_number)))

class JukeboxActions(flask.views.MethodView):
    def get(self):
        return json.dumps(actions.listActions())

