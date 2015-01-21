from flask import request, jsonify, render_template
from jukeboxModel import JukeboxModel

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
        

#class JukeboxAdd(flask.views.MethodView):
#    def post(self):
#        args = json.loads(request.data)
#        JukeboxModel.add_item(args['item'])
#        return jsonify({ 'success': True })
#
#class JukeboxRetrieve(flask.views.MethodView):
#    def get(self, n):
#        try:
#            n = int(n)
#        except ValueError:
#            n = RETRIEVE_DEFAULT_NR
#        if n <= 0:
#            n = RETRIEVE_DEFAULT_NR
#        jukeboxList = JukeboxModel.retrieve_last_N_items(n)
#        return jsonify({
#            'success': True,
#            'jukeboxList': [{ 'text': item } for item in jukeboxList]
#        })
