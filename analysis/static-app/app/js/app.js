// This will include ./node_modules/angular/angular.js
// and give us access to the `angular` global object.
require('angular/angular');
require('angular-ui-router/release/angular-ui-router');

// Create your app
var analysis = angular.module('analysis', ['ui.router']).config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    //
    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
        .state('home', {
            url: "/",
            templateUrl: "/static/analysis/partials/home.html",
            controller: "HomeController"
        })
        .state('tasks', {
            url: "/repo/{repo:.+}",
            templateUrl: "/static/analysis/partials/tasklist.html",
            // controller: "FileViewerController"
        })
        .state('repo', {
            url: "/repo/{repo:.+}/overview",
            templateUrl: "/static/analysis/partials/repo_overview.html",
            // controller: "FileViewerController"
        })
        .state('file', {
            url: "/commit/:commit/file/{filename:.+}",
            templateUrl: "/static/analysis/partials/file.html",
            controller: "FileViewerController"
        })

}]);

analysis.controller('HomeController', ['$scope', '$stateParams', '$http', function($scope, $stateParams, $http) {

  $scope.loading = true;

  $http.get('/api/repos')
    .success(function(res) {
        $scope.repos = res.repos;
    })
    .finally(function() {
      $scope.loading = false;
    });

}]);

analysis.controller('FileViewerController', ['$scope', '$stateParams', '$http', function($scope, $stateParams, $http) {

  $scope.filename = $stateParams.filename;
  $scope.commit = $stateParams.commit;

  $scope.loading = true

  $http.get('/api/commit/'+$scope.commit+'/file/'+$scope.filename)
    .success(function(res) {
      $scope.messages = {}
      res.pylint_analysis.forEach(function(message) {
        message.message = new Array(message.column + 1).join(' ') + message.message;
        if (message.line in $scope.messages) {
          $scope.messages[message.line-1].push(message)
        } else {
          $scope.messages[message.line-1] = [message]
        }
      })
      $scope.lines = res.raw_contents.split("\n").map(function(line, index) {
        return {
          text: line,
          messages: (index in $scope.messages) ? $scope.messages[index] : []
        }
      });
      
    })
    .finally(function() {
      $scope.loading = false;
    });

}]);
