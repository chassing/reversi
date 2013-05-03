import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace

logger = logging.getLogger("sockets.game")

from .models import Game
from .models import Move
from .models import Player
from .models import Socket


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
        # does not work :(
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
        self.log("{0.request.user.username} hits {1}".format(self, data))

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
            self.broadcast_grid()
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
        self.disconnect(silent=True)

    def broadcast_move(self, row, col, color):
        """
        """
        self.emit_to_game(self.game.pk, "set_cell", {
            "row": row,
            "col": col,
            "state": color
        })

    def broadcast_grid(self):
        try:
            # get the last move
            move = self.game.last_move
        except IndexError:
            move = Move(game=self.game)
            move.save()

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
        self.emit_to_game(self.game.pk, "players", [
            {
                'id': self.game.player1.pk,
                'name': self.game.player1.user.nickname,
                'color': self.game.player1.color,
            },
            {
                'id': self.game.player2.pk,
                'name': self.game.player2.user.nickname,
                'color': self.game.player2.color,
            },
        ])
        # update stats
        self.emit_to_game(self.game.pk, "statistics", {
            self.game.player1.pk: {
                'tiles': move.tiles_count(color=self.game.player1.color),
                'tiles_set': self.game.moves.filter(player=self.game.player1, passed=False).count(),
            },
            self.game.player2.pk: {
                'tiles': move.tiles_count(color=self.game.player2.color),
                'tiles_set': self.game.moves.filter(player=self.game.player2, passed=False).count(),

            },
            'move_count': self.game.moves.count()
        })
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

        # update the grid as last event
        self.emit_to_game(self.game.pk, "grid", move.grid())

    def _removed_staled_sessions(self):
        """ clean staled sockets
        """
        sessions = self.socket.server.sockets.keys()
        for socket in Socket.objects.all():
            if socket.session not in sessions:
                socket.delete()
