/* Project specific Javascript goes here. */

var reversiApp = angular.module('reversiApp', []);

reversiApp.controller("ReversiCtrl", function($scope, $log, $gameserver) {
    $scope.dynamic_buttons = null;
    $scope.players = null;
    $scope.current_player = {
        nickname: null,
        id: null
    };
    $scope.grid = [];
    $scope.end = false;

    /*
        click handler
    */
    $scope.hit_handler = function(tile) {
        $log.info(tile);
        if ($scope.end === true) {
            alert("Spiel ist zu Ende");
            return;
        }
        if ($scope.current_player.id !== window.player_id) {
            alert("Du bist nicht dran!");
            return;
        }
        if (tile.state !== "valid") {
            return;
        }
        $gameserver.emit("hit", tile);
    };

    $scope.button_handler = function(target) {
        $log.info("button:" + target);
        $gameserver.emit(target, {});
    };

    /*
        view helper
    */
    $scope.is_current_player = function(id) {
        if (id == $scope.current_player.id)
            return "info";
    };

    $scope.set_dynamic_buttons = function() {
        $scope.dynamic_buttons = [];
        // valid moves available
        pass = false;
        for (var i=0; i < $scope.grid.length; i++) {
            for (var j=0; j < $scope.grid[i].length; j++) {
                if ($scope.grid[i][j].state === 'valid') {
                    pass = true;
                    break;
                }
            }
        }
        if (pass === false && $scope.current_player.id == window.player_id && $scope.end !== true) {
            $log.info("add 'pass' button");
            $scope.dynamic_buttons.push({
                name: 'Passen',
                target: 'pass'
            });
        }
    };

    $scope.stats_sum = function(key) {
        i = 0;
        angular.forEach($scope.stats, function(value) {
            if (typeof value === 'object') {
                i = i + value[key];
            }

        });
        return i;
    };

    /*
        socketio event handler
    */
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

        $scope.set_dynamic_buttons();
    });

    $gameserver.on('end', function(data) {
        $scope.end = true;
        $scope.winner = data.name;
        alert("Spiel ist zu Ende - Gewinner:" + $scope.winner);
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
