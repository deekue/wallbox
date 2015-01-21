(function() {
	var app = angular.module('jukebox', []);

  app.controller('JukeboxController', ['$log', '$http', function($log, $http){
    var jukeCtrl = this;
    jukeCtrl.tracks = [];
    jukeCtrl.newTrack = {};
    jukeCtrl.origTracks = [];

    // TODO add support for mulitple wallboxes
    $log.log("grabbing track list");
    $http.get("/api/tracks/1").success(function(data){
      jukeCtrl.tracks = data.trackList;
    });

    this.showEditForm = function(index) {
      if(typeof jukeCtrl.tracks[index].showEditForm == "undefined") {
        jukeCtrl.tracks[index].showEditForm = true;
      }
      if(jukeCtrl.tracks[index].showEditForm) {
        jukeCtrl.tracks[index].showEditForm = false;
      } else {
        // now displaying the form, copy the original to enable reset()
        jukeCtrl.origTracks[index] = angular.copy(jukeCtrl.tracks[index]);
        jukeCtrl.tracks[index].showEditForm = true;
      }
    };

    this.isEditFormVisible = function(index) {
      if(typeof jukeCtrl.tracks[index].showEditForm == "undefined") {
        jukeCtrl.tracks[index].showEditForm = false;
      }
      return jukeCtrl.tracks[index].showEditForm;
    };

    this.editTrack = function(index) {
      newTrack = this.tracks[index];
      url = "/api/track/1/" + newTrack.letter + "/" + newTrack.number;
      $log.log("editTrack: url " + url);
      $http.post(url, newTrack).success(function(){
        jukeCtrl.showEditForm(index);
      }).error(function(data, status, headers, config){
        $log.log(data, status, headers, config);
      });
    };

    this.reset = function(index) {
      jukeCtrl.tracks[index] = angular.copy(jukeCtrl.origTracks[index]);
    };

  } ] );

  app.directive("jukeboxTabs", function() {
     return {
       restrict: "E",
       templateUrl: "static/jukebox-tabs.html",
       controller: function() {
         this.tab = 1;

         this.isSet = function(checkTab) {
           return this.tab === checkTab;
         };

         this.setTab = function(activeTab) {
           this.tab = activeTab;
         };
       },
       controllerAs: "tab"
     };
   });

	app.directive("jukeboxTracks", function() {
		return {
      restrict: 'E',
      templateUrl: "static/jukebox-tracks.html"
    };
  });
	app.directive("jukeboxSettings", function() {
		return {
      restrict: 'E',
      templateUrl: "static/jukebox-settings.html"
    };
  });
})();
