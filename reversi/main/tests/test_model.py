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
        # without moves player 1 is the next - should be an impossible situation
        self.assertEqual(self.game.next_player(), self.player1)
        # after first move (start constellation) player 1 is the next
        Move(game=self.game, player=self.player1).save()
        self.assertEqual(self.game.next_player(), self.player1)
        # player 2 is the next
        Move(game=self.game, player=self.player1).save()
        self.assertEqual(self.game.next_player(), self.player2)
        # player 1 is the next
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

        C = self.player1.color.name
        M = self.player2.color.name

        self.start_field = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]

    def test_start_constellation(self):
        move = Move(game=self.game, player=self.player1)
        move.save()

        self.assertEqual(move.field, _(self.start_field))

    def test_grid(self):
        pass

    def test_valid_north(self):
        move = Move(game=self.game, player=self.player2, field=_(self.start_field))
        move.save()
        self.assertTrue(move.is_valid_cell(row=5, col=3, color=self.player1.color.name))

    def test_valid_north_east(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, C, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F))
        move.save()
        self.assertTrue(move.is_valid_cell(row=5, col=2, color=C))

    def test_valid_east(self):
        move = Move(game=self.game, player=self.player2, field=_(self.start_field))
        move.save()
        self.assertTrue(move.is_valid_cell(row=3, col=5, color=self.player1.color.name))

    def test_valid_south_east(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, M, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F))
        move.save()
        self.assertTrue(move.is_valid_cell(row=2, col=2, color=M))

    def test_valid_south(self):
        move = Move(game=self.game, player=self.player1, field=_(self.start_field))
        move.save()
        self.assertTrue(move.is_valid_cell(row=2, col=3, color=self.player2.color.name))

    def test_valid_south_west(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, C, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F))
        move.save()
        self.assertTrue(move.is_valid_cell(row=2, col=5, color=C))

    def test_valid_west(self):
        move = Move(game=self.game, player=self.player1, field=_(self.start_field))
        move.save()
        self.assertTrue(move.is_valid_cell(row=3, col=2, color=self.player2.color.name))

    def test_valid_north_west(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, M, E, E, E, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F))
        move.save()
        self.assertTrue(move.is_valid_cell(row=5, col=5, color=M))

    def test_not_valid_all_empty(self):
        move = Move(game=self.game, player=self.player2, field=_(self.start_field))
        move.save()
        self.assertTrue(not move.is_valid_cell(row=0, col=0, color=self.player1.color.name))

    def test_not_valid_outside(self):
        move = Move(game=self.game, player=self.player2, field=_(self.start_field))
        move.save()
        self.assertTrue(not move.is_valid_cell(row=9, col=0, color=self.player1.color.name))

    def test_not_valid(self):
        move = Move(game=self.game, player=self.player2, field=_(self.start_field))
        move.save()
        self.assertTrue(not move.is_valid_cell(row=2, col=3, color=self.player1.color.name))
