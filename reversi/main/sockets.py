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

    def log(self, message, level=logging.INFO):
        logger.log(level, "[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, data):
        """ user is joining a game
        """
        self.game = Game.objects.get(pk=data["id"], players=self.request.user)
        self.log("{0.request.user.username} is joining the game {0.game.pk}".format(self))

        self.player = Player.objects.get(game=self.game, user=self.request.user)
        self.player.sockets.add(Socket(session=self.socket.sessid))
        self.player.save()

        self.socket.session['user'] = self.request.user
        self.broadcast_connected_players()
        self.broadcast_grid()

    def on_hit(self, data):
        """ player hits a valid cell
        """
        self.log("{0.request.user.username} hits {1}".format(self, data))

        if self.game.next_player() != self.player:
            self.log("{0.request.user.username} is a cheater".format(self))
            # someone tries to cheat or duplicated socket.io requests :(
            return

        # create new move
        move = Move(game=self.game, player=self.player)
        move.field = self.game.last_move().field
        if move.is_valid_cell(row=data['row'], col=data['col'], color=self.player.color.name):
            move.set_cell(row=data['row'], col=data['col'], color=self.player.color.name)
            # save changes
            move.save()
            self.broadcast_grid()

    def on_pass(self, data):
        """ now valid cells available so the player passes
        """
        self.log("{0.request.user.username} pass".format(self))

        if self.game.next_player() != self.player:
            self.log("{0.request.user.username} is a cheater".format(self))
            # someone tries to cheat or duplicated socket.io requests :(
            return

        # create new move
        move = Move(game=self.game, player=self.player, passed=True)
        move.field = self.game.last_move().field
        # save changes
        move.save()
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
        self.broadcast_connected_players()
        self.disconnect(silent=True)

    def broadcast_connected_players(self):
        self._removed_staled_sessions()
        connected_players = 0
        for p in self.game.players.all():
            connected_players += p.sockets.count()
        self.log("connected players: {0}".format(connected_players), level=logging.DEBUG)
        self.broadcast_event('connected_players', {"value": connected_players})

    def broadcast_grid(self):
        try:
            # get the last move
            move = self.game.last_move()
        except IndexError:
            move = Move(game=self.game)
            move.save()
        # set current player
        next = self.game.next_player()
        self.broadcast_event("current_player", {
            "nickname": next.user.nickname,
            "id": next.user.pk
        })
        # update players
        self.broadcast_event("players", [
            {
                'id': self.game.player1.pk,
                'name': self.game.player1.user.nickname,
                'color': self.game.player1.color.name,
            },
            {
                'id': self.game.player2.pk,
                'name': self.game.player2.user.nickname,
                'color': self.game.player2.color.name,
            },
        ])
        # update stats
        self.broadcast_event("statistics", {
            self.game.player1.pk: {
                'tiles': move.tiles_count(color=self.game.player1.color.name),
                'tiles_set': self.game.moves.filter(player=self.game.player1, passed=False).count(),
            },
            self.game.player2.pk: {
                'tiles': move.tiles_count(color=self.game.player2.color.name),
                'tiles_set': self.game.moves.filter(player=self.game.player2, passed=False).count(),

            },
            'move_count': self.game.moves.count()
        })
        # update the grid as last event
        self.broadcast_event("grid", move.grid())

    def _removed_staled_sessions(self):
        """ clean staled sockets
        """
        sessions = self.socket.server.sockets.keys()
        for socket in Socket.objects.all():
            if socket.session not in sessions:
                socket.delete()
