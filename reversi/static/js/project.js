/* Project specific Javascript goes here. */

angular.module('reversi', [])
    .controller("ReversiCtrl", function($scope, $game) {
        $scope.connected_players = 0;
        $scope.field = {};

/*        $scope.is_valid_cell = function($event) {
            console.log($event.target.id);
            $game.emit("is_valid_cell", {id: $event.target.id});
        };*/

        $scope.update = function() {
            $game.emit("update", {});
        };

        $game.on('connect', function(data) {
            $game.emit("join", {id: window.game_id});
        });

        $game.on('connected_players', function(data) {
            console.log("connected_players", data);
            $scope.connected_players = data.value;
        });

        $game.on('update_field', function(data) {
            console.log("update_field", data);
            $scope.field = data;
            for (var item in $scope.field) {
                if ($scope.field[item].valid === true) {
                    $("#" + item).addClass("field-cell-valid");
                } else {
                    $("#" + item).removeClass("field-cell-valid");
                }
                if ($scope.field[item].player1 === true) {
                    $("#" + item).addClass("field-cell-player1");
                } else {
                    $("#" + item).removeClass("field-cell-player1");
                }
                if ($scope.field[item].player2 === true) {
                    $("#" + item).addClass("field-cell-player2");
                } else {
                    $("#" + item).removeClass("field-cell-player2");
                }
            }
        });

        //$scope.speed = 1;
        //$scope.$watch('speed', function(newVal) {
        //    $socketio.emit("new_speed", parseFloat(newVal));
        //});
//
        //$scope.clik_data = [];
        //$socketio.on('clik', function(data) {
        //    console.log("CLIK", data);
        //    $scope.clik_data.push(data);
        //});
    })
.factory('$game', function ($rootScope) {
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
