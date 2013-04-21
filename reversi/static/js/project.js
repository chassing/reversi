/* Project specific Javascript goes here. */

var reversiApp = angular.module('reversiApp', []);

reversiApp.controller("ReversiCtrl", function($scope, $log, $gameserver) {
    $scope.connected_players = 0;
    $scope.players = null;
    $scope.current_player = {
        nickname: null,
        id: null
    };
    $scope.grid = [];

    $scope.hit = function(tile) {
        $log.info(tile);
        if ($scope.current_player.id !== window.user_id) {
            alert("Du bist nicht dran!");
            return;
        }
        if (tile.state !== "valid") {
            return;
        }
        $gameserver.emit("hit", tile);
    };

    $scope.is_current_player = function(id) {
        if (id == $scope.current_player.id)
            return "info";
    };
    $gameserver.on('connect', function(data) {
        $gameserver.emit("join", {id: window.game_id});
    });

    $gameserver.on('players', function(data) {
        $log.info("players", data);
        $scope.players = data;
    });

    $gameserver.on('statistics', function(data) {
        $log.info("statistics", data);
        $scope.stats = data;
    });

    $gameserver.on('current_player', function(data) {
        $log.info("current_player", data);
        $scope.current_player = data;
    });

    $gameserver.on('grid', function(data) {
        $log.info("grid", data);
        $scope.grid = data;
    });

    $gameserver.on('cheater', function(data) {
        $log.info("cheater", data);
        alert("Aber aber aber, das will ich nicht nochmal sehen!");
    });
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
