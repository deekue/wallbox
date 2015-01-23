// pagination code snippet from: http://plnkr.co/edit/AD1AGCYIm1dZhbuoPhxX?p=preview

(function() {
	var app = angular.module('jukebox', ['ui.bootstrap', 'ngResource']);

  app.factory('trackFactory', function($resource) {
  });

  app.controller('JukeboxController', ['$scope', '$log', '$resource', function($scope, $log, $resource){
    var jukeCtrl = this;
    // TODO add support for mulitple wallboxes
    var TrackList = $resource('/api/track/:wallbox/:letter/:number', {wallbox:1});
    $log.log("grabbing track list");
    $scope.tracks = TrackList.query(); //TODO add error handler
    $scope.newTrack = {};
    $scope.origTracks = [];
    $scope.currentPage = 1;
    $scope.itemsPerPage = 10;

    // pagination
    $scope.tracks.$promise.then(function () {
      $scope.totalItems = $scope.tracks.length;
      $scope.$watch('currentPage + itemsPerPage', function() {
        var begin = (($scope.currentPage - 1) * $scope.itemsPerPage),
          end = begin + $scope.itemsPerPage;
        $scope.filteredTracks = $scope.tracks.slice(begin, end);
      });
    });

    this.showEditForm = function(index) {
      if(typeof $scope.tracks[index].showEditForm == "undefined") {
        $scope.tracks[index].showEditForm = true;
      }
      if($scope.tracks[index].showEditForm) {
        $scope.tracks[index].showEditForm = false;
      } else {
        // now displaying the form, copy the original to enable reset()
        $scope.origTracks[index] = angular.copy($scope.tracks[index]);
        $scope.tracks[index].showEditForm = true;
      }
    };

    this.isEditFormVisible = function(index) {
      if(typeof $scope.tracks[index].showEditForm == "undefined") {
        $scope.tracks[index].showEditForm = false;
      }
      return $scope.tracks[index].showEditForm;
    };

    this.editTrack = function(index) {
      track_letter = $scope.tracks[index].letter;
      track_number = $scope.tracks[index].number;
      newTrack = angular.copy($scope.tracks[index]);
      //$scope.tracks[index].$save({letter:track_letter, number:track_number}, function(){
      newTrack.$save({letter:track_letter, number:track_number}, function(){
        jukeCtrl.showEditForm(index);
      }, function(httpResponse){
        $log.log(httpResponse);
      });
    };

    this.reset = function(index) {
      $scope.tracks[index] = angular.copy($scope.origTracks[index]);
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
