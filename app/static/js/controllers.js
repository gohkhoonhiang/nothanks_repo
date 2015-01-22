nothanksApp.controller('PlayerController', ['$rootScope','$scope','$location','$http','$interval',
  function($rootScope, $scope, $location, $http, $interval) {
    $scope.createPlayer = function() {
      $scope.message = '';
      $http.post('/nothanks/api/v1.0/app/players/create/', {'player_name':$scope.player_name}).
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          return $location.path('/rooms');
        }).
        error(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          $scope.message = message;
        });
    };
}]);

nothanksApp.controller('RoomController', ['$rootScope','$scope','$location','$http','$interval',
  function($rootScope, $scope, $location, $http, $interval) {

    var show_rooms = function() {
      $http.get('/nothanks/api/v1.0/app/rooms/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          $scope.rooms = output;
        });
      $http.get('/nothanks/api/v1.0/app/players/current/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          $scope.current_player = output['name'];
        });
    };

    $interval(show_rooms, 1000);
    
    $scope.createRoom = function() {
      $scope.message = '';
      $http.post('/nothanks/api/v1.0/app/rooms/create/', {'room_name':$scope.room_name}).
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          $scope.room_id = output['id'];
          $scope.room_name = '';
          show_rooms();
        }).
        error(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          $scope.room_id = output['id'];
          $scope.room_name = '';
          $scope.message = message;
          show_rooms();
        });
    };

    $scope.joinRoom = function(room_id) {
      $http.post('/nothanks/api/v1.0/app/p/join/', {'room_id':room_id}).
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          if (result == 'fail') {
            $rootScope.message = message;
          } else {
            return $location.path('/game');
          }
        });
    };

    $scope.leaveLobby = function() {
      $http.delete('/nothanks/api/v1.0/app/players/remove/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          if (result == 'fail') {
            $rootScope.message = message;
          } else {
            return $location.path('/');
          }
        });
    };
}]);

nothanksApp.controller('GameController', ['$rootScope','$scope','$location','$http','$interval',
  function($rootScope, $scope, $location, $http, $interval) {
  
    var game_state = function(state) {
      var message = '';
      switch(state) {
        case 'waiting_player':
          message = 'Waiting for players...';
          break;
        case 'ready_to_start':
          message = 'Ready to start game...';
          break;
        case 'draw_card':
          message = 'Next player to draw card...';
          break;
        case 'take_or_pay':
          message = 'Take the card or pay a chip...';
          break;
        case 'calculate_points':
          message = 'Calculating points...';
          break;
        default:
          message = 'Unknown state...';
          break;
      }
      return message;
    }
  
    var show_room = function() {
      $http.get('/nothanks/api/v1.0/app/rooms/current/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          $scope.room = output;
          $scope.game_players = output['players'];
          $scope.top_card = output['top_card'];
          $scope.current_chips = output['current_chips'];
          $scope.cards = output['cards'].length;
          $scope.game_state = game_state(output['state']);
        });
	  $http.get('/nothanks/api/v1.0/app/p/nextplayer/').
		success(function(data, status, headers, config) {
		  var result = data['result'];
		  var code = data['code'];
		  var message = data['message'];
		  var output = data['output'];
		  $scope.next_player = output['name'];
		});
      $http.get('/nothanks/api/v1.0/app/players/current/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          $scope.current_player = output['name'];
        });
    };

    $interval(show_room, 1000);

    $scope.startGame = function() {
      $http.post('/nothanks/api/v1.0/app/p/start/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
        });
    };

    $scope.leaveRoom = function() {
      $http.post('/nothanks/api/v1.0/app/p/leave/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
          if (result == 'fail') {
            $rootScope.message = message;
          } else {
            return $location.path('/rooms');
          }
        });
    };

    $scope.drawCard = function() {
      $http.post('/nothanks/api/v1.0/app/p/draw/').
        success(function(data, status, headers, config) {
          var result = data['result'];
          var code = data['code'];
          var message = data['message'];
          var output = data['output'];
        });
    };
}]);

