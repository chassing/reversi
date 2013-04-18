from django.test import TestCase


from main.models import Game
from main.models import Move
from main.models import CELL_EMPTY as E
#from models import CELL_VALID as V


def _(f):
    return ",".join(f)


class GameTest(TestCase):
    fixtures = ['test-user-data.json']

    def setUp(self):
        self.game = Game.objects.get(pk=1)
        self.player1 = self.game.players.all()[0]
        self.player2 = self.game.players.all()[1]

    def test_next_player(self):
        """ get the next player
        """
        self.assertEqual(self.game.next_player(), self.player1)
        Move(game=self.game, player=self.player1).save()
        self.assertEqual(self.game.next_player(), self.player2)
        Move(game=self.game, player=self.player2).save()
        self.assertEqual(self.game.next_player(), self.player1)

    def test_last_move(self):
        """ get the last move
        """
        move = Move(game=self.game, player=self.player1)
        move.save()
        self.assertEqual(self.game.last_move(), move)

        move = Move(game=self.game, player=self.player2)
        move.save()
        self.assertEqual(self.game.last_move(), move)


class MoveTest(TestCase):
    fixtures = ['test-user-data.json']

    def setUp(self):
        self.game = Game.objects.get(pk=1)
        self.player1 = self.game.players.all()[0]
        self.player2 = self.game.players.all()[1]

    def test_start_constellation(self):
        """ test start constellation
        """
        C = self.player1.color.name
        M = self.player2.color.name

        F1 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1)
        move.save()

        self.assertEqual(move.field, _(F1))

    def test_valid(self):
        """ test if selected cell is a valid cell
        """
        pass
