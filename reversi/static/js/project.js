/* Project specific Javascript goes here. */

var reversiApp = angular.module('reversiApp', ['$strap.directives']);

reversiApp.controller("ReversiCtrl", function($scope, $log, $gameserver, $modal) {
    $scope.default_buttons = [{
        name: 'Aufgeben',
        target: 'surrender'
    }];
    $scope.dynamic_buttons = null;
    $scope.players = null;
    $scope.current_player = {
        nickname: null,
        id: null
    };
    $scope.grid = [];
    $scope.game_end = false;
    $scope.update_grid = true;
    $scope.skin = window.skin;

    /*
        click handler
    */
    $scope.hit_handler = function(tile) {
        $log.info(tile);
        if ($scope.game_end === true) {
            alert("Spiel ist zu Ende");
            return;
        }
        if ($scope.current_player.id !== window.player_id) {
            alert("Du bist nicht dran!");
            return;
        }
        if (tile.state !== "v") {
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
    $scope.highlight_current_player = function(id) {
        if ($scope.is_current_player(id))
            return "alert-success";
        return "alert-default";
    };

    $scope.is_current_player = function(id) {
        if (id == $scope.current_player.id)
            return true;
        return false;
    };

    $scope.is_player = function(id) {
        if (id == window.player_id)
            return true;
        return false;
    };

    $scope.set_dynamic_buttons = function() {
        $scope.dynamic_buttons = $scope.default_buttons;
        // valid moves available
        pass = false;
        for (var i=0; i < $scope.grid.length; i++) {
            for (var j=0; j < $scope.grid[i].length; j++) {
                if ($scope.grid[i][j].state === 'v') {
                    pass = true;
                    break;
                }
            }
        }
        if (pass === false && $scope.current_player.id == window.player_id && $scope.game_end !== true) {
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

    $gameserver.on('set_cell', function(data) {
        $log.info("set_cell", data);
        $scope.grid[data.row][data.col] = data;
        // disable grid updates for a moment
        $scope.update_grid = false;
        setTimeout(function () {
            $scope.update_grid = true;
        }, 1000);
    });

    $scope._grid_callback = function(data) {
        $log.info("grid", data);
        if ($scope.update_grid === true) {
            $log.info("updating grid");
            $scope.grid = data;
            $scope.set_dynamic_buttons();
        } else {
            setTimeout(function() {
                $log.info("not updating grid ... ");
                $scope.$apply(function () {
                    $scope._grid_callback(data);
                });
            }, 400);
        }
    };

    $gameserver.on('grid', $scope._grid_callback);

    $gameserver.on('end', function(data) {
        $log.info("game end", data);
        $scope.game_end = true;
        $scope.winner = data.name;
        var modal = $modal({
          template: 'winner.html',
          show: true,
          backdrop: 'static',
          scope: $scope
        });
    });

    $gameserver.on('cheater', function(data) {
        $log.info("cheater", data);
        alert("Aber aber aber, das will ich nicht nochmal sehen!");
    });
});

reversiApp.factory('$gameserver', function ($rootScope) {
    if (window.client_socketio === "disabled")
        return {
            on: function (eventName, callback) { return; },
            emit: function (eventName, callback) { return; }
        };

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
            '<div class="field-cell skin-{{ skin }}-field-cell-state-{{ tile.state }}"></div>',
        scope: {
            tile: '=',
            skin: '='
        }
    };
});
