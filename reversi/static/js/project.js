/* Project specific Javascript goes here. */

var reversiApp = angular.module('reversiApp', []);

reversiApp.controller("ReversiCtrl", function($scope, $log, $gameserver) {
    $scope.connected_players = 0;
    $scope.grid = [];

/*        $scope.is_valid_cell = function($event) {
        console.log($event.target.id);
        $game.emit("is_valid_cell", {id: $event.target.id});
    };*/

    $scope.update = function() {
        $gameserver.emit("update", {});
    };

    $scope.hit = function(tile) {
        $log.info(tile);
        $gameserver.emit("hit", tile);
    };

    $gameserver.on('connect', function(data) {
        $gameserver.emit("join", {id: window.game_id});
    });

    $gameserver.on('connected_players', function(data) {
        $log.info("connected_players", data);
        $scope.connected_players = data.value;
    });

    $gameserver.on('update_field', function(data) {
        $log.info("update_field", data);
        $scope.grid = data;
    });

    //$scope.speed = 1;
    //$scope.$watch('speed', function(newVal) {
    //    $socketio.emit("new_speed", parseFloat(newVal));
    //});
});

reversiApp.factory('$gameserver', function ($rootScope) {
    if (window.client_socketio === "disabled")
        return {};

    var socket = io.connect("/game");
    return {
        on: function (eventName, callback) {
            socket.on(eventName, function () {
                var args = arguments;
                $rootScope.$apply(function () {
                    callback.apply(socket, args);
                });
            });
        },
        emit: function (eventName, data, callback) {
            socket.emit(eventName, data, function () {
                var args = arguments;
                $rootScope.$apply(function () {
                    if (callback) {
                        callback.apply(socket, args);
                    }
                });
            });
        }
    };
});

reversiApp.directive('reversiField', function() {
    return {
        restrict:
            'E',
        template:
            '<div class="field-cell field-cell-state-{{ tile.state }}"></div>',
        scope: {
            tile: '='
        }
    };
});
