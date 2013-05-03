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

    $scope.selected_row = undefined;
    $scope.selected_column = undefined;

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

    $scope.handle_keypress = function(key) {
        if (key < 13) return;
        if (key > 13 && (key < 49 || key > 72)) return;
        if (56 < key && key < 65) return;

        $log.info("key: " +  key);

        if ($scope.current_player.id !== window.player_id) {
            alert("Du bist nicht dran!");
            return;
        }

        if (key >= 49 && key <= 56) {
            // select row
            if ($scope.selected_column !== undefined) {
                $scope.selected_row = key - 49;
            }
        }
        if (key >= 65 && key <= 72) {
            $scope.selected_column = key - 65;
            $scope.selected_row = undefined;
        }

        if (key == 13 && $scope.selected_column !== undefined && $scope.selected_row !== undefined) {
            // hit
            $gameserver.emit("hit", {
                row: $scope.selected_row,
                col: $scope.selected_column
            });
            $scope.selected_column = undefined;
            $scope.selected_row = undefined;
        }
    };

    $scope.highlight_selected_column = function(tile) {
        if (tile.col === $scope.selected_column) {
            return "skin-" + $scope.skin + "-selected";
        }
        return "";
    };

    $scope.highlight_selected_row = function(row) {
        if (row === $scope.selected_row) {
            return "skin-" + $scope.skin + "-selected";
        }
        return "";
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

    $gameserver.on('invalid_move', function(data) {
        alert("Dieser Zug ist nicht erlaubt");
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

reversiApp.directive('onKeyupFn', function() {
    return function(scope, elm, attrs) {
        //Evaluate the variable that was passed
        //In this case we're just passing a variable that points
        //to a function we'll call each keyup
        var keyupFn = scope.$eval(attrs.onKeyupFn);
        elm.bind('keyup', function(evt) {
            //$apply makes sure that angular knows
            //we're changing something
            scope.$apply(function() {
                keyupFn.call(scope, evt.which);
            });
        });
    };
});
