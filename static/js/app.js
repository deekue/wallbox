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
    $scope.newTrack = {}; //edit form
    $scope.origTracks = []; // for form reset
    $scope.currentPage = 1; // pagination
    $scope.itemsPerPage = 10; //pagination

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
        $scope.filteredTracks[index].showEditForm = true;
      }
      if($scope.filteredTracks[index].showEditForm) {
        $scope.filteredTracks[index].showEditForm = false;
      } else {
        // now displaying the form, copy the original to enable reset()
        $scope.origTracks[index] = angular.copy($scope.filteredTracks[index]);
        $scope.filteredTracks[index].showEditForm = true;
      }
    };

    this.isEditFormVisible = function(index) {
      if(typeof $scope.filteredTracks[index].showEditForm == "undefined") {
        $scope.filteredTracks[index].showEditForm = false;
      }
      return $scope.filteredTracks[index].showEditForm;
    };

    this.editTrack = function(index) {
      track_letter = $scope.filteredTracks[index].letter;
      track_number = $scope.filteredTracks[index].number;
      newTrack = angular.copy($scope.filteredTracks[index]);
      newTrack.$save({letter:track_letter, number:track_number}, function(){
        jukeCtrl.showEditForm(index);
      }, function(httpResponse){
        $log.log(httpResponse);
      });
    };

    this.reset = function(index) {
      $scope.filteredTracks[index] = angular.copy($scope.origTracks[index]);
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
