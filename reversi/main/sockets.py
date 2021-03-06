import logging
import gevent

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace

logger = logging.getLogger("sockets.game")

from .models import Game
from .models import Move
from .models import Player
from .models import Socket
from .models import CELL_VALID
from .models import AI_EASY, AI_MEDIUM, AI_HARD


@namespace('/game')
class GameNamespace(BaseNamespace, BroadcastMixin):

    def initialize(self):
        self.log("Socketio session started")
        if 'games' not in self.session:
            self.session['games'] = set()

    def log(self, message, level=logging.INFO):
        logger.log(level, "[{0}] {1}".format(self.socket.sessid, message))

    def join(self, game):
        self.session['games'].add(game)

    def leave(self, game):
        self.session['games'].remove(game)

    def emit_to_game(self, game, event, *args):
        """ This is sent to all in the game
        (in this particular Namespace)
        """
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'games' not in socket.session:
                continue
            if game in socket.session['games']:
                socket.send_packet(pkt)

    def on_join(self, data):
        """ user is joining a game
        """
        self.game = Game.objects.get(pk=data["id"], players__user=self.request.user)
        self.log("{0.request.user.username} is joining the game {0.game.pk}".format(self))
        self.join(self.game.pk)

        self.player = Player.objects.get(game=self.game, user=self.request.user)
        self.player.sockets.add(Socket(session=self.socket.sessid))
        self.player.save()

        self.socket.session['user'] = self.request.user
        self._removed_staled_sessions()
        self.broadcast_grid()

    def on_hit(self, data):
        """ player hits a valid cell
        """
        self.log("{0.request.user.username} hits {1}".format(self, data), level=logging.DEBUG)

        if self.game.next_player != self.player:
            self.log("{0.request.user.username} is a cheater".format(self))
            # someone tries to cheat or duplicated socket.io requests :(
            return

        # create new move
        move = Move(game=self.game, player=self.player)
        move.field = self.game.last_move.field
        if move.is_valid_cell(row=data['row'], col=data['col'], color=self.player.color):
            self.broadcast_move(row=data['row'], col=data['col'], color=self.player.color)
            move.set_cell(row=data['row'], col=data['col'], color=self.player.color)
            # save changes
            move.save()

            gevent.spawn_later(1, self.broadcast_grid)
        else:
            self.emit("invalid_move", {})

    def on_pass(self, data):
        """ now valid cells available so the player passes
        """
        self.log("{0.request.user.username} pass".format(self))

        if self.game.next_player != self.player:
            self.log("{0.request.user.username} is a cheater".format(self))
            # someone tries to cheat or duplicated socket.io requests :(
            return

        # create new move
        move = Move(game=self.game, player=self.player, passed=True)
        move.field = self.game.last_move.field
        # save changes
        move.save()
        self.broadcast_grid()

    def on_deny(self, data):
        """ user denied this game
        """
        self.log("{0.request.user.username} deny".format(self))
        self.player.denied = True
        self.player.save()
        self.broadcast_grid()

    def on_surrender(self, data):
        """ player surrendered
        """
        self.log("{0.request.user.username} surrender".format(self))
        self.player.surrendered = True
        self.player.save()
        self.broadcast_grid()

    def recv_disconnect(self):
        """ browser disconnect
        """
        self.log('Disconnected')
        self.log("session: {0.socket.sessid} user: {0.request.user}".format(self))
        try:
            socket = Socket.objects.get(session=self.socket.sessid, player__user=self.request.user)
            socket.delete()
        except Socket.DoesNotExist:
            pass
        self.leave(self.game.pk)
        self._removed_staled_sessions()
        self.broadcast_grid()
        self.disconnect(silent=True)

    def ai_callback(self, row, col, player):
        """ will be executed from game model after the computer turn
        """
        if row and col:
            self.broadcast_move(row=row, col=col, color=player.color)
        gevent.spawn_later(2, self.broadcast_grid)

    def broadcast_move(self, row, col, color):
        """
        """
        self.emit_to_game(self.game.pk, "set_cell", {
            "row": row,
            "col": col,
            "state": color
        })

    def broadcast_grid(self):
        # refresh game object
        self.game = Game.objects.get(pk=self.game.pk)

        # get the last move
        move = self.game.last_move

        if self.game.next_player:
            # set current player
            self.emit_to_game(self.game.pk, "current_player", {
                "nickname": self.game.next_player.user.nickname,
                "id": self.game.next_player.pk
            })
        else:
            self.emit_to_game(self.game.pk, "current_player", {
                "nickname": None,
                "id": None
            })

        # update players
        player1_connected = False
        player2_connected = False
        if self.game.player1.sockets.count() > 0 or self.game.player1.user.is_ai:
            player1_connected = True
        if self.game.player2.sockets.count() > 0 or self.game.player2.user.is_ai:
            player2_connected = True
        self.emit_to_game(self.game.pk, "players", [
            {
                'id': self.game.player1.pk,
                'name': self.game.player1.user.nickname,
                'color': self.game.player1.color,
                'connected': player1_connected,
            },
            {
                'id': self.game.player2.pk,
                'name': self.game.player2.user.nickname,
                'color': self.game.player2.color,
                'connected': player2_connected,
            },
        ])

        # update stats
        self.emit_to_game(self.game.pk, "statistics", {
            self.game.player1.pk: {
                'tiles': move.tiles_count(color=self.game.player1.color),
                'tiles_set': self.game.moves.filter(player=self.game.player1, passed=False).count() - 1,
            },
            self.game.player2.pk: {
                'tiles': move.tiles_count(color=self.game.player2.color),
                'tiles_set': self.game.moves.filter(player=self.game.player2, passed=False).count(),

            },
            'move_count': self.game.moves.count() - 1
        })

        if self.game.next_player and self.game.next_player.user.is_ai:
            # get the level from the username
            me = self.game.next_player
            if me.user.username == "computer_easy":
                level = AI_EASY
            elif me.user.username == "computer_medium":
                level = AI_MEDIUM
            else:
                level = AI_HARD

            if self.game.player1 == self.game.next_player:
                opponent = self.game.player2
            else:
                opponent = self.game.player1

            # let the AI 'think' about the next move
            gevent.spawn_later(2, self.game.ai, level=level, me=me, opponent=opponent, callback=self.ai_callback)

        current_grid = move.grid()

        # game end?
        if self.game.end:
            self.log("game ended")
            if self.game.winner:
                winner = {
                    "name": self.game.winner.user.nickname,
                    "id": self.game.winner.pk
                }
            else:
                winner = {
                    "name": "unentschieden",
                    "id": 0
                }
            self.log("winner {0}".format(winner["name"]))
            self.emit_to_game(self.game.pk, "end", winner)
        else:
            pass_btn_for_player_id = self.game.next_player.pk
            for row in current_grid:
                for cell in row:
                    if cell["state"] == CELL_VALID:
                        pass_btn_for_player_id = 0
                        break
            if pass_btn_for_player_id == self.game.next_player.pk:
                self.log("show pass button")

            # set buttons
            self.emit_to_game(self.game.pk, "update_buttons", {
                'pass_btn_for_player_id': pass_btn_for_player_id,
            })

        # update the grid as last event
        self.emit_to_game(self.game.pk, "grid", current_grid)

    def _removed_staled_sessions(self):
        """ clean staled sockets
        """
        sessions = self.socket.server.sockets.keys()
        for socket in Socket.objects.all():
            if socket.session not in sessions:
                socket.delete()
