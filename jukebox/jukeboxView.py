from flask import request, jsonify, render_template
from jukeboxModel import JukeboxModel, generate_tracks

import flask.views
import json

class JukeboxView(flask.views.MethodView):
    def get(self):
        return render_template('index.html')

class JukeboxPlay(flask.views.MethodView):
    def get(self, wallbox, letter, number):
        # TODO add action code here
        print "play track %s%s for wallbox %s" % (letter, number, wallbox)
        return jsonify(success=True)

class JukeboxTracks(flask.views.MethodView):
    def get(self, wallbox):
        trackList = JukeboxModel.retrieve_tracks(wallbox)
        #return json.dumps(trackList)
        return jsonify(
            success=True,
            trackList=trackList)

class JukeboxTrack(flask.views.MethodView):
    def get(self, wallbox, letter, number):
        track = JukeboxModel.retrieve_track(wallbox, letter, number)
        return jsonify(track)

    def post(self, wallbox, letter, number):
        track = json.loads(request.data)
        JukeboxModel.update_track(track)
        return jsonify(success=True)
        
class JukeboxGenTracks(flask.views.MethodView):
    def get(self, wallbox, highest_letter, highest_number):
        generate_tracks(wallbox, highest_letter, highest_number)
        return "Generated tracks for wallbox:%d from A1 to %s%s" % (wallbox,
                highest_letter, highest_number)

