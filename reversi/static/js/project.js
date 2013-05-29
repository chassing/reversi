/* Project specific Javascript goes here. */

var reversiApp = angular.module('reversiApp', ['$strap.directives']);

reversiApp.controller("ReversiCtrl", function($scope, $log, $gameserver, $modal) {
    $scope.default_buttons = {
        surrender: {
            name: 'Aufgeben',
            target: 'surrender',
            disabled: false,
            cls: 'btn-danger'
        },
        pass: {
            name: 'Passen',
            target: 'pass',
            disabled: true,
            cls: 'btn-primary'
    }};

    // set default
    $scope.btns = angular.copy($scope.default_buttons);

    $scope.players = [{
        id: 0,
        name: '',
        color: '1',
        connected: false
    },{
        id: 1,
        name: '',
        color: '2',
        connected: false
    }];

    $scope.stats = {
        0: {
            tiles: 0,
            tiles_set: 0
        },
        1: {
            tiles: 0,
            tiles_set: 0
        },
        move_count: 0
    };

    $scope.current_player = {
        nickname: null,
        id: null
    };

    $scope.grid = [
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}],
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}],
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}],
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}],
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}],
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}],
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}],
        [{state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}, {state: 'e'}]
    ];

    $scope.game_end = false;
    $scope.update_grid = true;
    $scope.theme = window.theme;

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
        $scope.selected_column = undefined;
        $scope.selected_row = undefined;
    };

    $scope.button_class = function(target) {
        if(target.disabled === true) {
            return "";
        } else {
            return target.cls;
        }

    }

    $scope.button_handler = function(target) {
        $log.info("button:" + target);
        $gameserver.emit(target, {});
    };

    /*
        view helper
    */
    $scope.highlight_current_player = function(id) {
        if ($scope.is_current_player(id))
            return "alert-info";
        return "alert-default";
    };

    $scope.is_current_player = function(id) {
        if (id == $scope.current_player.id)
            return true;
        return false;
    };

    $scope.is_player = function(player) {
        if (player.id == window.player_id)
            return true;
        return false;
    };

    $scope.is_not_connected = function(player) {
        if (player.connected === false)
            return true;
        return false;
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
            if (key != 13) {
                alert("Du bist nicht dran!");
            }
            return;
        }

        if (key >= 49 && key <= 56) {
            $scope.selected_row = key - 49;
        }
        if (key >= 65 && key <= 72) {
            $scope.selected_column = key - 65;
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
            return "theme-" + $scope.theme + "-selected";
        }
        return "";
    };

    $scope.highlight_selected_row = function(row) {
        if (row === $scope.selected_row) {
            return "theme-" + $scope.theme + "-selected";
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
    });

    $gameserver.on('grid', function(data) {
        $log.info("grid", data);
        $scope.grid = data;
    });

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

    $gameserver.on('update_buttons', function(data) {
        if ($scope.game_end === true) {
            return;
        }

        // set default
        $scope.btns = angular.copy($scope.default_buttons);

        if (data.pass_btn_for_player_id === window.player_id) {
            $log.info("enable 'pass' button");
            $scope.btns.pass.disabled = false;
        }
    });
});

reversiApp.factory('$gameserver', function ($rootScope) {
    if (window.client_socketio === "disabled")
        return {
            on: function (eventName, callback) { return; },
            emit: function (eventName, callback) { return; }
        };

    var socket = io.connect("/game", {'sync disconnect on unload' : true});
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

reversiApp.directive('tooltip', function () {
    return {
        restrict:
            'A',
        link: function(scope, element, attrs) {
            $(element)
                .attr('title', attrs.tooltip)
                .tooltip({placement: "left"});
        }
    };
});
