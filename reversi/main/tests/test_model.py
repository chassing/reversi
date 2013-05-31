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
        self.assertEqual(Move.objects.count(), 0)
        # without moves player 1 is the next - should be an impossible situation
        self.assertEqual(self.game.next_player, self.player1)
        # after first move (start constellation) player 1 is the next
        Move(game=self.game, player=self.player1).save()
        self.assertEqual(Move.objects.count(), 1)
        self.assertEqual(self.game.next_player, self.player1)
        # player 2 is the next
        Move(game=self.game, player=self.player1).save()
        self.assertEqual(self.game.next_player, self.player2)
        # player 1 is the next
        Move(game=self.game, player=self.player2).save()
        self.assertEqual(self.game.next_player, self.player1)

    def test_last_move(self):
        """ get the last move
        """
        move = Move(game=self.game, player=self.player1)
        move.save()
        self.assertEqual(self.game.last_move, move)

        move = Move(game=self.game, player=self.player2)
        move.save()
        self.assertEqual(self.game.last_move, move)

    def test_no_end(self):
        Move(game=self.game, player=self.player1).save()
        self.assertTrue(not self.game.end)

    def test_end_last_two_moves_passed(self):
        Move(game=self.game, player=self.player1, passed=True).save()
        Move(game=self.game, player=self.player2, passed=True).save()
        self.assertTrue(self.game.end)

    def test_end_no_empty_cell(self):
        C = self.player1.color
        M = self.player2.color
        F1 = [
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            M, M, M, C, C, C, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
        ]
        Move(game=self.game, player=self.player1, field=_(F1)).save()
        self.assertTrue(self.game.end)

    def test_end_player1_surrender(self):
        self.player1.surrendered = True
        self.player1.save()
        self.assertTrue(self.game.end)

    def test_end_player2_surrender(self):
        self.player2.surrendered = True
        self.player2.save()
        self.assertTrue(self.game.end)

    def test_winner_player1_surrender(self):
        self.player1.surrendered = True
        self.player1.save()
        self.assertEqual(self.game.winner, self.player2)

    def test_winner_player2_surrender(self):
        self.player2.surrendered = True
        self.player2.save()
        self.assertEqual(self.game.winner, self.player1)

    def test_stats_player1_winner(self):
        C = self.player1.color
        M = self.player2.color
        F1 = [
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
        ]
        Move(game=self.game, player=self.player1, field=_(F1)).save()
        # refresh objects from db
        self.player1 = self.game.players.all()[0]
        self.player2 = self.game.players.all()[1]

        self.assertEqual(self.player1.user.games_won, 1)
        self.assertEqual(self.player1.user.score, 2 * 5 * 33)
        self.assertEqual(self.player2.user.games_lost, 1)
        self.assertEqual(self.player2.user.score, 5 * 31)

    def test_stats_player2_winner(self):
        C = self.player1.color
        M = self.player2.color
        F1 = [
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
        ]
        Move(game=self.game, player=self.player1, field=_(F1)).save()
        # refresh objects from db
        self.player1 = self.game.players.all()[0]
        self.player2 = self.game.players.all()[1]

        self.assertEqual(self.player2.user.games_won, 1)
        self.assertEqual(self.player2.user.score, 2 * 5 * 33)
        self.assertEqual(self.player1.user.games_lost, 1)
        self.assertEqual(self.player1.user.score, 5 * 31)

    def test_stats_player1_denied(self):
        self.player1.denied = True
        self.player1.save()

        self.assertEqual(self.player1.user.games_won, 0)
        self.assertEqual(self.player1.user.games_lost, 0)
        self.assertEqual(self.player1.user.score, 0)
        self.assertEqual(self.player2.user.games_won, 0)
        self.assertEqual(self.player2.user.games_lost, 0)
        self.assertEqual(self.player2.user.score, 0)

    def test_stats_player2_denied(self):
        self.player2.denied = True
        self.player2.save()

        self.assertEqual(self.player1.user.games_won, 0)
        self.assertEqual(self.player1.user.games_lost, 0)
        self.assertEqual(self.player1.user.score, 0)
        self.assertEqual(self.player2.user.games_won, 0)
        self.assertEqual(self.player2.user.games_lost, 0)
        self.assertEqual(self.player2.user.score, 0)

    def test_stats_player1_surrendered(self):
        C = self.player1.color
        M = self.player2.color
        F1 = [
            E, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
        ]
        Move(game=self.game, player=self.player1, field=_(F1)).save()
        self.player1.surrendered = True
        self.player1.save()

        # refresh objects from db
        self.player1 = self.game.players.all()[0]
        self.player2 = self.game.players.all()[1]

        self.assertEqual(self.player1.user.games_lost, 1)
        self.assertEqual(self.player1.user.games_surrendered, 1)
        self.assertEqual(self.player1.user.score, 5 * 31)
        self.assertEqual(self.player2.user.games_won, 1)
        self.assertEqual(self.player2.user.score, 2 * 5 * 32)

    def test_stats_player2_surrendered(self):
        C = self.player1.color
        M = self.player2.color
        F1 = [
            E, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            C, C, C, C, C, C, C, C,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
            M, M, M, M, M, M, M, M,
        ]
        Move(game=self.game, player=self.player1, field=_(F1)).save()
        self.player2.surrendered = True
        self.player2.save()

        # refresh objects from db
        self.player1 = self.game.players.all()[0]
        self.player2 = self.game.players.all()[1]

        self.assertEqual(self.player1.user.games_won, 1)
        self.assertEqual(self.player1.user.score, 2 * 5 * 31)
        self.assertEqual(self.player2.user.games_lost, 1)
        self.assertEqual(self.player2.user.games_surrendered, 1)
        self.assertEqual(self.player2.user.score, 5 * 32)

    def test_winner_player1(self):
        C = self.player1.color
        F1 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, C, E, E,
            E, E, E, C, C, C, E, E,
            E, E, E, C, C, C, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player1, field=_(F1))
        move.save()
        move = Move(game=self.game, player=self.player2, passed=True)
        move.field = self.game.last_move.field
        move.save()
        move = Move(game=self.game, player=self.player1, passed=True)
        move.field = self.game.last_move.field
        move.save()
        self.assertTrue(self.game.end)
        self.assertEqual(self.game.winner, self.player1)

    def test_winner_player2(self):
        M = self.player2.color
        F1 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, M, M, M, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player2, field=_(F1))
        move.save()
        move = Move(game=self.game, player=self.player1, passed=True)
        move.field = self.game.last_move.field
        move.save()
        move = Move(game=self.game, player=self.player2, passed=True)
        move.field = self.game.last_move.field
        move.save()
        self.assertTrue(self.game.end)
        self.assertEqual(self.game.winner, self.player2)

    def test_winner_draw(self):
        M = self.player2.color
        C = self.player1.color
        F1 = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, C, C, M, M, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        move = Move(game=self.game, player=self.player2, field=_(F1))
        move.save()
        move = Move(game=self.game, player=self.player1, passed=True)
        move.field = self.game.last_move.field
        move.save()
        move = Move(game=self.game, player=self.player2, passed=True)
        move.field = self.game.last_move.field
        move.save()
        self.assertEqual(self.game.winner, None)

    def test_end_player1_denied(self):
        self.player1.denied = True
        self.player1.save()
        self.assertTrue(self.game.end)
        self.assertEqual(self.game.winner, None)

    def test_end_player2_denied(self):
        self.player2.denied = True
        self.player2.save()
        self.assertTrue(self.game.end)
        self.assertEqual(self.game.winner, None)

    def test_ai_random(self):
        C = self.player1.color
        M = self.player2.color
        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, C, E, E, E, E,
            E, E, E, M, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        Move.objects.create(game=self.game, player=self.player2, field=_(F))
        self.assertEqual(self.game.ai_random(self.player1), (3, 3))

        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, C, E, E, E, E,
            E, E, C, M, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        Move.objects.create(game=self.game, player=self.player2, field=_(F))
        self.assertTrue(self.game.ai_random(self.player1) in [(3, 3), (2, 4)])

        F = [
            E, E, E, E, E, E, E, E,
            E, E, C, C, E, E, E, E,
            E, E, C, M, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        Move.objects.create(game=self.game, player=self.player2, field=_(F))
        self.assertTrue(self.game.ai_random(self.player1) in [(3, 3), (2, 4), (3, 4)])

    def test_ai_ramscher(self):
        C = self.player1.color
        M = self.player2.color
        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        Move.objects.create(game=self.game, player=self.player2, field=_(F))
        self.assertTrue(self.game.ai_ramscher(me=self.player1, opponent=self.player2) in [(2, 4), (3, 5), (4, 2), (5, 3)])

        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, C, C, C, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        Move.objects.create(game=self.game, player=self.player1, field=_(F))
        self.assertTrue(self.game.ai_ramscher(me=self.player2, opponent=self.player2) in [(2, 5)])

        F = [
            E, E, C, C, C, E, E, E,
            E, E, M, E, E, E, E, E,
            C, C, C, C, C, C, E, E,
            M, M, M, M, M, M, E, E,
            C, C, C, M, C, C, C, E,
            C, E, M, E, E, E, E, E,
            E, M, M, M, M, E, E, E,
            M, E, M, E, C, E, E, E,
        ]
        Move.objects.create(game=self.game, player=self.player2, field=_(F))
        self.assertTrue(self.game.ai_ramscher(me=self.player1, opponent=self.player2) in [(5, 4)])

    def test_ai_minimax(self):
        C = self.player1.color
        M = self.player2.color
        F = [
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, C, M, E, E, E,
            E, E, E, M, C, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
            E, E, E, E, E, E, E, E,
        ]
        Move.objects.create(game=self.game, player=self.player2, field=_(F))
        self.assertTrue(self.game.ai_minimax(me=self.player1, opponent=self.player2) in [(2, 4), (3, 5), (4, 2), (5, 3)])


class MoveTest(TestCase):
    fixtures = ['test-user-data.json']

    def setUp(self):
        self.game = Game.objects.get(pk=1)
        self.player1 = self.game.players.all()[0]
        self.player2 = self.game.players.all()[1]

        C = self.player1.color
        M = self.player2.color

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
        C = self.player1.color
        M = self.player2.color
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
        move.set_cell(row=5, col=2, color=self.player1.color)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_set_cell_no_turn_cells(self):
        C = self.player1.color
        M = self.player2.color
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
        move.set_cell(row=5, col=2, color=self.player1.color, turn_cells=False)
        move.save()
        self.assertEqual(move.field, _(F2))

    def test_turn_cells_north(self):
        C = self.player1.color
        M = self.player2.color
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
        C = self.player1.color
        M = self.player2.color
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
        C = self.player1.color
        M = self.player2.color
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
        C = self.player1.color
        M = self.player2.color
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
        C = self.player1.color
        M = self.player2.color
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
        C = self.player1.color
        M = self.player2.color
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
        C = self.player1.color
        M = self.player2.color
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
        self.assertTrue(move.is_valid_cell(row=5, col=3, color=self.player1.color))

    def test_valid_north_east(self):
        C = self.player1.color
        M = self.player2.color
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
        self.assertTrue(move.is_valid_cell(row=3, col=5, color=self.player1.color))

    def test_valid_south_east(self):
        C = self.player1.color
        M = self.player2.color
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
        self.assertTrue(move.is_valid_cell(row=2, col=3, color=self.player2.color))

    def test_valid_south_west(self):
        C = self.player1.color
        M = self.player2.color
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
        self.assertTrue(move.is_valid_cell(row=3, col=2, color=self.player2.color))

    def test_valid_north_west(self):
        C = self.player1.color
        M = self.player2.color
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
        B = self.player1.color
        W = self.player2.color
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
        self.assertTrue(not move.is_valid_cell(row=0, col=0, color=self.player1.color))

    def test_not_valid_outside(self):
        move = Move(game=self.game, player=self.player2, field=_(self.start_field))
        move.save()
        self.assertTrue(not move.is_valid_cell(row=9, col=0, color=self.player1.color))

    def test_not_valid(self):
        move = Move(game=self.game, player=self.player2, field=_(self.start_field))
        move.save()
        self.assertTrue(not move.is_valid_cell(row=2, col=3, color=self.player1.color))
