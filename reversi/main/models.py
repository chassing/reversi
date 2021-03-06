import logging
log = logging.getLogger("main.models")

from random import randint
from collections import defaultdict

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver, Signal


CELL_VALID = "v"
CELL_EMPTY = "e"
CELL_PLAYER1 = "1"
CELL_PLAYER2 = "2"

AI_EASY = "easy"
AI_MEDIUM = "medium"
AI_HARD = "hard"
AI_DEPTH = 3

INFINITY = 999999999

FIELD_SCORES = [
    [9999, 5, 500, 200, 200, 500, 5, 9999],
    [5, 1, 50, 150, 150, 50, 1, 5],
    [500, 50, 250, 100, 100, 250, 50, 500],
    [200, 150, 100, 50, 50, 100, 150, 200],
    [200, 150, 100, 50, 50, 100, 150, 200],
    [500, 50, 250, 100, 100, 250, 50, 500],
    [5, 1, 50, 150, 150, 50, 1, 5],
    [9999, 5, 500, 200, 200, 500, 5, 9999],
]

WINNER_BONUS = 2
TILES_SCORE = 5


class NoValidMoveException(Exception):
    pass


def get_default_theme():
    return Theme.objects.get(pk=1)


class Theme(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, default="")
    player1 = models.CharField(max_length=254, help_text="player 1 css class")
    player2 = models.CharField(max_length=254, help_text="player 2 css class")
    field = models.CharField(max_length=254, blank=True, help_text="game field css class")

    def __unicode__(self):
        return self.description


class ReversiUser(AbstractUser):
    nickname = models.CharField(max_length=254, verbose_name='Spitzname')
    theme = models.ForeignKey(Theme, null=True, default=get_default_theme, verbose_name="Thema")
    is_ai = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    games_surrendered = models.IntegerField(default=0)

    def __unicode__(self):
        return self.nickname

    @property
    def games_count(self):
        return self.games_won + self.games_lost


class Game(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField(default=8)
    created = models.DateTimeField(auto_now=True, auto_now_add=True)
    end = models.BooleanField(default=False)

    @property
    def next_player(self):
        if self.end:
            return None

        if self.moves.count() <= 1:
            # player 1 is the first on
            return self.player1

        try:
            last_move = self.last_move
        except IndexError:
            return self.player1

        # who is the next player
        next = self.player2 if last_move.player == self.player1 else self.player1
        return next

    @property
    def last_move(self):
        try:
            return self.moves.reverse()[0]
        except IndexError:
            return Move.objects.create(game=self, player=self.player1)

    @property
    def winner(self):
        if not self.end:
            raise Exception("Game not ended")

        if self.player1.winner:
            return self.player1
        if self.player2.winner:
            return self.player2

        # draw
        return None

    @property
    def player1(self):
        return self.players.all()[0]

    @property
    def player2(self):
        return self.players.all()[1]

    @property
    def denyable(self):
        if self.end:
            return False
        if self.moves.count() > 2:
            return False
        return True

    def ai(self, level, me, opponent, callback):
        """ call the AI and make a move
        """
        try:
            if level == AI_EASY:
                row, col = self.ai_random(me)
            elif level == AI_MEDIUM:
                row, col = self.ai_ramscher(me, opponent)
            elif level == AI_HARD:
                row, col = self.ai_minimax(me, opponent)
            move = Move(
                game=self,
                player=me,
                field=self.last_move.field,
            )
            move.set_cell(row=row, col=col, color=me.color)
        except NoValidMoveException:
            row = col = None
            move = Move(
                game=self,
                player=me,
                field=self.last_move.field,
                passed=True
            )

        # save changes
        move.save()
        # computer is done
        callback(row, col, me)

    def score_move(self, move, me, opponent=None):
        score = 0
        for row in xrange(0, self.size):
            for col in xrange(0, self.size):
                if move.get_cell(row, col) == me.color:
                    score += FIELD_SCORES[row][col]
                elif opponent and move.get_cell(row, col) == opponent.color:
                    score -= FIELD_SCORES[row][col]
        return score

    def ai_random(self, me):
        """ AI easy - random
        """
        valid_cells = self.last_move.valid_cells(color=me.color)
        if not valid_cells:
            raise NoValidMoveException()
        cell = valid_cells[randint(0, len(valid_cells) - 1)]
        return cell[0], cell[1]

    def ai_ramscher(self, me, opponent, with_score=False):
        """ AI medium - something like greedy algorithm
        """
        if not self.last_move.valid_cells(color=me.color):
            raise NoValidMoveException()

        max_score = -999999
        best_moves = defaultdict(list)
        for child in self.last_move.next_states(me):
            log.debug("scoring {0}".format(child))

            # now score this move
            score = self.score_move(child, me, opponent)

            log.debug("{} with {}".format(child, score))
            if score >= max_score:
                log.debug("{} >= {}".format(score, max_score))
                best_moves[score].append((child.row, child.col))
                max_score = score

        if with_score:
            return (max_score, best_moves[max_score][randint(0, len(best_moves[max_score]) - 1)])

        # get a random move from all with max_score
        return best_moves[max_score][randint(0, len(best_moves[max_score]) - 1)]

    def ai_minimax(self, me, opponent):
        """ AI hard - minimax algorithm
        """
        valid_cells = self.last_move.valid_cells(color=me.color)
        if not valid_cells:
            raise NoValidMoveException()

        score, move = self.minimax(self.last_move, depth=AI_DEPTH, me=me, opponent=opponent)
        log.debug("AI: {}, {} with {}".format(move.row, move.col, score))
        return move.row, move.col

    def minimax(self, move, depth, me, opponent, alfa=-INFINITY, beta=INFINITY):
        if depth == 0:
            return (self.score_move(move, me), move)

        best_move = move

        for child in move.next_states(me):
            score, _ = self.minimax(child, depth-1, opponent, me, -beta, -alfa)
            score = -score
            if score > alfa:
                log.debug("depth: {} new best score {}".format(depth, score))
                alfa = score
                best_move = child
            if beta <= alfa:
                break
        return (self.score_move(move, me), best_move)

    def __unicode__(self):
        return "{0.pk} - {0.name}".format(self)


class Player(models.Model):
    COLOR_CHOICES = (
        (CELL_PLAYER1, 'black'),
        (CELL_PLAYER2, 'white'),
    )
    user = models.ForeignKey(ReversiUser)
    game = models.ForeignKey(Game, related_name="players")
    surrendered = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    winner = models.BooleanField(default=False)
    color = models.CharField(max_length=1, choices=COLOR_CHOICES)

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return "{0.user.username} - {0.game}".format(self)

    def save(self, *args, **kwargs):
        super(Player, self).save(*args, **kwargs)
        if self.surrendered or self.denied:
            log.info("{0.user.nickname} surrendered or denied".format(self))
            game_end.send(sender=self, game=self.game)


class Move(models.Model):
    field = models.TextField()
    row = models.IntegerField(default=0)
    col = models.IntegerField(default=0)
    player = models.ForeignKey(Player, related_name="moves", null=True)
    game = models.ForeignKey(Game, related_name="moves")
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    passed = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)

    def grid(self):
        """ get grid representation for the next player

        [
          [XXX,XXX,XXX, ... ,XXX]
          ...
          [XXX,XXX,XXX, ... ,XXX]
        ]
        """
        def _get_row(row, move):
            r = []
            for col, state in enumerate(move):
                if not self.game.end and state == CELL_EMPTY and self.is_valid_cell(row, col, self.game.next_player.color):
                    state = CELL_VALID
                r.append({
                    "state": state,
                    "row": row,
                    "col": col,
                })
            return r

        grid = []
        for row in xrange(0, self.game.size):
            row_start = row*self.game.size
            field_part = self.field.split(",")[row_start:row_start+self.game.size]
            grid.append(_get_row(row, field_part))
        return grid

    def set_cell(self, row, col, color, turn_cells=True, update_row_col=True):
        """ place a 'tile'
        """
        if update_row_col:
            self.row = row
            self.col = col
        field_list = list(self.field.split(","))
        field_list[row*self.game.size+col] = color
        self.field = ",".join(field_list)
        # turn cells
        if turn_cells:
            self.turn_cells(row, col, color)

    def get_cell(self, row, col):
        """ return 'tile' on select place
        """
        return self.field.split(",")[row*self.game.size+col]

    def turn_cells(self, row, col, color):
        for direction in [(-1, -1), (-1, +0), (-1, +1),
                          (+0, -1),           (+0, +1),
                          (+1, -1), (+1, +0), (+1, +1)]:
            if self.get_cell(row, col) is not CELL_EMPTY:
                self._turn_cells_one_direction(row, col, direction, color)

    def _turn_cells_one_direction(self, row, col, direction, color):
        """ turn tiles
        """
        dy = direction[0]
        dx = direction[1]
        c = col + dx
        r = row + dy

        # flipping only possible if there is an own stone "behind" them
        possible = False
        while self.in_game_field(r, c):
            if self.get_cell(r, c) == CELL_EMPTY:
                # empty field behind enemy stones, but no own stone
                return
            if self.get_cell(r, c) == color:
                # own stone found -> enemy stones are flipped up to this point
                possible = True
                break
            # we found an enemy tile, go further into this direction
            c += dx
            r += dy

        # flip stones in this direction until you get to an own tile
        if possible:
            c = col + dx
            r = row + dy
            while self.in_game_field(r, c) and self.get_cell(r, c) not in (color, CELL_EMPTY):
                #log.debug("Flipping {},{}".format(r, c))
                self.set_cell(r, c, color, turn_cells=False, update_row_col=False)
                c += dx
                r += dy

    def in_game_field(self, row, col):
        return row >= 0 and col >= 0 and row <= self.game.size-1 and col <= self.game.size-1

    def is_valid_cell(self, row, col, color):
        """ is the cell valid for given user
        """
        if not self.in_game_field(row, col):
            # row, col outside
            return False

        if self.get_cell(row=row, col=col) != CELL_EMPTY:
            # not an empty cell
            return False

        # find enemy in neighbors cells
        for test_row, test_col in [(row-1, col-1), (row-1, col), (row-1, col+1),
                                   (row, col-1),                 (row, col+1),
                                   (row+1, col-1), (row+1, col), (row+1, col+1)]:
            if not self.in_game_field(test_row, test_col):
                continue
            if self.get_cell(row=test_row, col=test_col) in (color, CELL_EMPTY):
                continue

            # enemy tile found, now search for my own tile in this direction
            while True:
                if row - test_row < 0:
                    # is the next row
                    test_row += 1
                elif row - test_row > 0:
                    # is the previous row
                    test_row -= 1
                if col - test_col < 0:
                    # is the next col
                    test_col += 1
                elif col - test_col > 0:
                    # is the previous col
                    test_col -= 1

                if not self.in_game_field(test_row, test_col):
                    # outside
                    break
                if self.get_cell(row=test_row, col=test_col) == CELL_EMPTY:
                    break
                if self.get_cell(row=test_row, col=test_col) == color:
                    # enemy tile found
                    return True
                # another enemy tile found, go further
        return False

    def valid_cells(self, color):
        """ returns a list of tuples with valid cells for the next move
        """
        vc = []
        for row in xrange(0, self.game.size):
            for col in xrange(0, self.game.size):
                if self.is_valid_cell(row, col, color):
                    vc.append((row, col))
        return vc

    def next_states(self, player):
        """ return a list of possible completed moves and their coordinates
        """
        moves = []
        for row, col in self.valid_cells(player.color):
            move = Move(game=self.game, player=player, field=self.field)
            move.set_cell(row, col, player.color)
            moves.append(move)
        return moves

    def tiles_count(self, color):
        return self.field.count(color)

    def save(self, *args, **kwargs):
        if not self.field:
            # start constellation
            self.field = ",".join([CELL_EMPTY] * self.game.size**2)
            # place player1
            self.set_cell(row=(self.game.size/2)-1, col=(self.game.size/2)-1,
                          color=self.game.player1.color,
                          turn_cells=False)
            self.set_cell(row=self.game.size/2, col=self.game.size/2,
                          color=self.game.player1.color,
                          turn_cells=False)
            # place player2
            self.set_cell(row=(self.game.size/2)-1, col=self.game.size/2,
                          color=self.game.player2.color,
                          turn_cells=False)
            self.set_cell(row=self.game.size/2, col=(self.game.size/2)-1,
                          color=self.game.player2.color,
                          turn_cells=False)

        # save
        super(Move, self).save(*args, **kwargs)

        # game ends
        # * if last 2 moves are passed
        # * if no empty cells are available
        if self.game.moves.count() >= 2 and \
                self.game.moves.reverse()[0].passed and \
                self.game.moves.reverse()[1].passed or \
                CELL_EMPTY not in self.field:
            game_end.send(sender=self, game=self.game)

    def print_human_readable_grid(self):
        grid = []
        for r in xrange(0, self.game.size):
            grid.append([self.get_cell(r, c) for c in xrange(0, self.game.size)])
        for row in grid:
            print " ".join(row)

    def __unicode__(self):
        return "{0.row}, {0.col} ({0.game})".format(self)


class Socket(models.Model):
    session = models.CharField(max_length=128)
    player = models.ForeignKey(Player, related_name="sockets")

    def __unicode__(self):
        return "{0.session} - {0.player.user.username}".format(self)


game_end = Signal(providing_args=["game"])


@receiver(game_end, dispatch_uid="game_end_handler")
def game_end_handler(sender, game, **kwargs):
    if game.end:
        # already set
        return

    log.info("{} game ends".format(game.pk))

    # set end
    game.end = True
    game.save()

    # now get the winner
    player1 = game.player1
    player2 = game.player2

    if player1.denied or player2.denied:
        # no stats if someone denied this game
        return

    tiles_player1 = game.last_move.tiles_count(color=player1.color)
    tiles_player2 = game.last_move.tiles_count(color=player2.color)

    # someone surrendered?
    if player1.surrendered:
        # player2 wins
        winner = player2
        winner_tiles = tiles_player2
        loser = player1
        loser_tiles = tiles_player1
    elif player2.surrendered:
        # player1 wins
        winner = player1
        winner_tiles = tiles_player1
        loser = player2
        loser_tiles = tiles_player2
    elif tiles_player2 > tiles_player1:
        # player2 has more tiles
        winner = player2
        winner_tiles = tiles_player2
        loser = player1
        loser_tiles = tiles_player1
    elif tiles_player1 > tiles_player2:
        # player1 has more tiles
        winner = player1
        winner_tiles = tiles_player1
        loser = player2
        loser_tiles = tiles_player2
    else:
        log.info("{} is draw".format(game.pk))
        return

    log.info("winner: {0.user} loser: {1.user}".format(winner, loser))

    # set winner flag
    winner.winner = True

    # update stats
    winner.user.games_won += 1
    loser.user.games_lost += 1

    if player1.surrendered or player2.surrendered:
        log.info("{0.user} surrendered".format(loser))
        loser.user.games_surrendered += 1

    # update scores
    winner.user.score += WINNER_BONUS * TILES_SCORE * winner_tiles
    loser.user.score += TILES_SCORE * loser_tiles

    # save
    winner.user.save()
    winner.save()
    loser.user.save()
    loser.save()
