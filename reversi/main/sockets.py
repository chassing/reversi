import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace

logger = logging.getLogger("sockets.game")

from .models import Game
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

    def on_update(self, data):
        """ helper
        """
        import random
        field = {}
        for row in xrange(0, 8):
            for col in xrange(0, 8):
                r = random.randint(0, 2)
                if r == 0:
                    player1 = True
                    player2 = False
                elif r == 1:
                    player1 = False
                    player2 = True
                else:
                    player1 = False
                    player2 = False

                field["cell_{0}_{1}".format(row, col)] = {
                    "player1": player1,
                    "player2": player2,
                    "valid": False if not random.randint(0, 1) else True,
                }
        self.emit("update_field", field)

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

    def _removed_staled_sessions(self):
        """ clean staled sockets
        """
        sessions = self.socket.server.sockets.keys()
        for socket in Socket.objects.all():
            if socket.session not in sessions:
                socket.delete()
