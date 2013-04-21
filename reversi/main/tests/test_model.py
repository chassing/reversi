from django.test import TestCase


from main.models import Game
from main.models import Move
from main.models import CELL_EMPTY as E


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

    def test_set_cell_turn_cells(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, C, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        F2 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, C, E, E,
            E, E, E, C, C, E, E, E,
            E, E, E, C, C, E, E, E,
            E, E, C, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=5, col=2, color=self.player1.color.name)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_set_cell_no_turn_cells(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, C, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        F2 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, C, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, C, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=5, col=2, color=self.player1.color.name, turn_cells=False)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_north(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            C, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        F2 = [
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=7, col=0, color=C)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_south(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            E, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            M, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
        ]
        F2 = [
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
            C, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=0, col=0, color=C)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_east(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            E, M, M, M, M, M, M, C,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        F2 = [
            C, C, C, C, C, C, C, C,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=0, col=0, color=C)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_west(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            C, M, M, M, M, M, M, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        F2 = [
            C, C, C, C, C, C, C, C,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=0, col=7, color=C)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_east_and_west(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            C, M, M, E, M, M, M, C,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        F2 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            C, C, C, C, C, C, C, C,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=3, col=3, color=C)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_north_east_south_and_west(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            E, E, E, C, E, E, E, E,
            E, E, E, M, E, E, E, E,
            E, E, E, M, E, E, E, E,
            C, M, M, M, M, M, M, C,
            E, E, E, M, E, E, E, E,
            E, E, E, M, E, E, E, E,
            E, E, E, M, E, E, E, E,
            E, E, E, C, E, E, E, E,
        ]
        F2 = [
            E, E, E, C, E, E, E, E,
            E, E, E, C, E, E, E, E,
            E, E, E, C, E, E, E, E,
            C, C, C, C, C, C, C, C,
            E, E, E, C, E, E, E, E,
            E, E, E, C, E, E, E, E,
            E, E, E, C, E, E, E, E,
            E, E, E, C, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=3, col=3, color=C)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_all_directions(self):
        C = self.player1.color.name
        M = self.player2.color.name
        F1 = [
            C, E, E, C, E, E, C, E,
            M, M, E, M, E, M, E, E,
            M, E, M, M, M, E, E, E,
            C, M, M, M, M, M, M, C,
            M, E, M, M, M, E, E, M,
            M, M, E, M, E, M, E, M,
            C, E, E, M, E, E, M, M,
            E, E, E, C, E, E, E, C,
        ]
        F2 = [
            C, E, E, C, E, E, C, E,
            M, C, E, C, E, C, E, E,
            M, E, C, C, C, E, E, E,
            C, C, C, C, C, C, C, C,
            M, E, C, C, C, E, E, M,
            M, C, E, C, E, C, E, M,
            C, E, E, C, E, E, C, M,
            E, E, E, C, E, E, E, C,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.set_cell(row=3, col=3, color=C)
        move.save()
        self.assertEqual(move.field, _(F2))

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

    def test_valid_bug_found(self):
        B = self.player1.color.name
        W = self.player2.color.name
        F = [
            W, W, W, B, E, E, B, E,
            W, W, B, B, E, E, B, E,
            W, W, B, B, B, B, B, E,
            W, W, B, W, B, B, E, E,
            E, W, E, B, W, W, E, E,
            E, E, B, W, W, W, E, E,
            E, B, E, W, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F))
        move.save()
        self.assertTrue(not move.is_valid_cell(row=6, col=0, color=W))
        self.assertTrue(not move.is_valid_cell(row=6, col=2, color=W))
        self.assertTrue(move.is_valid_cell(row=4, col=2, color=W))
        self.assertTrue(move.is_valid_cell(row=5, col=1, color=W))

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
