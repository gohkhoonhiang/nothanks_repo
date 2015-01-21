'use strict';

var nothanksApp = angular.module('nothanksApp', ['ngRoute']);

nothanksApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        controller: 'PlayerController',
        templateUrl: '../static/partials/home.html'
      }).
      when('/rooms', {
        controller: 'RoomController',
        templateUrl: '../static/partials/rooms.html'
      }).
      when('/game', {
        controller: 'GameController',
        templateUrl: '../static/partials/game.html'
      }).
      otherwise({
        redirectTo: '/'
      });
  }
]);