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
        player = Player.objects.get(game=self.game, user=self.request.user)
        player.sockets.add(Socket(session=self.socket.sessid))
        player.save()
        self.socket.session['user'] = self.request.user
        self.broadcast_connected_players()
        self.broadcast_grid()

    def on_hit(self, data):
        """ helper
        """
        player = Player.objects.get(game=self.game, user=self.request.user)
        move = Move(game=self.game, player=player)
        last_move = Move.objects.filter(game=self.game).reverse()[0]
        move.field = last_move.field
        move.set_cell(row=data['row'], col=data['col'], tile=player.color.name)
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
        for p in Player.objects.filter(game=self.game):
            connected_players += p.sockets.count()
        self.log("connected players: {0}".format(connected_players), level=logging.DEBUG)
        self.broadcast_event('connected_players', {"value": connected_players})

    def broadcast_grid(self):
        try:
            # get the last move
            move = Move.objects.filter(game=self.game).reverse()[0]
        except IndexError:
            player = Player.objects.get(game=self.game, user=self.request.user)
            move = Move(game=self.game, player=player)
            move.save()
        self.broadcast_event("update_field", move.grid())

    def _removed_staled_sessions(self):
        """ clean staled sockets
        """
        sessions = self.socket.server.sockets.keys()
        for socket in Socket.objects.all():
            if socket.session not in sessions:
                socket.delete()
