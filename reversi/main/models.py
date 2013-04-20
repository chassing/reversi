import logging

log = logging.getLogger("main.models")

from django.db import models
from django.contrib.auth.models import AbstractUser


CELL_VALID = "valid"
CELL_EMPTY = "empty"


class ReversiUser(AbstractUser):
    nickname = models.CharField(max_length=254)


class TileColor(models.Model):
    name = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class Game(models.Model):
    #players = models.ManyToManyField(ReversiUser, through='Player')
    size = models.IntegerField(default=8)

    def next_player(self):
        players = self.players.all()
        player1 = players[0]
        player2 = players[1]

        if self.moves.count() == 1:
            # player 1 is the first on
            return player1

        try:
            last_move = self.last_move()
        except IndexError:
            return player1

        # who is the next player
        next = player2 if last_move.player == player1 else player1
        return next

    def last_move(self):
        return self.moves.reverse()[0]

    def __unicode__(self):
        return "{0.pk}".format(self)


class Player(models.Model):
    user = models.ForeignKey(ReversiUser)
    game = models.ForeignKey(Game, related_name="players")
    color = models.ForeignKey(TileColor)

    def __unicode__(self):
        return "{0.user.username} - {0.game} - {0.color}".format(self)


class Move(models.Model):
    field = models.TextField()
    player = models.ForeignKey(Player, related_name="moves")
    game = models.ForeignKey(Game, related_name="moves")
    date = models.DateTimeField(auto_now=True, auto_now_add=True)

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
                if state == CELL_EMPTY and self.is_valid_cell(row, col, self.game.next_player().color.name):
                    state = CELL_VALID
                r.append({
                    "state": state,
                    "row": row,
                    "col": col,
                })
            return r

        grid = []
        for row in xrange(0, self.game.size):
            grid.append(_get_row(row, self.field.split(",")[row*self.game.size:row*self.game.size+self.game.size]))
        return grid

    def set_cell(self, row, col, tile):
        """ place a 'tile'
        """
        field_list = list(self.field.split(","))
        field_list[row*self.game.size+col] = tile
        self.field = ",".join(field_list)

    def get_cell(self, row, col):
        """ return 'tile' on select place
        """
        return self.field.split(",")[row*self.game.size+col]

    def turn_cells(self, row, col, color):
        if self.get_cell(row, col) not in (CELL_EMPTY, CELL_VALID):
            self.turn_cells_one_direction(row, col, -1, -1, color)
            self.turn_cells_one_direction(row, col, -1, 0, color)
            self.turn_cells_one_direction(row, col, -1, 1, color)
            self.turn_cells_one_direction(row, col, 0, -1, color)
            self.turn_cells_one_direction(row, col, 0, 1, color)
            self.turn_cells_one_direction(row, col, 1, -1, color)
            self.turn_cells_one_direction(row, col, 1, 0, color)
            self.turn_cells_one_direction(row, col, 1, 1, color)

    def turn_cells_one_direction(self, row, col, dx, dy, color):
        """ turn tiles
        """
        c = col + dx
        r = row + dy
        # amount of enemy stones
        amt = 0
        # flipping only possible if there is an own stone "behind" them
        possible = False
        #log.debug("New Tile: {},{}, direction {},{}".format(row, col, dy, dx))
        while self.in_game_field(r, c):
            #log.debug("Testing {},{}".format(r, c))
            if self.get_cell(r, c) not in (CELL_EMPTY, CELL_VALID):
                if self.get_cell(r, c) != color:
                    amt += 1
                else:
                    # own stone found -> enemy stones are flipped up to this point
                    possible = True
                    break
            else:
                # empty/valid field behind enemy stones, but no own stone
                return
            c += dx
            r += dy

        # flip stones in this direction until you get to an empty/valid/own field
        if possible:
            c = col + dx
            r = row + dy
            while self.in_game_field(r, c) and self.get_cell(r, c) not in (color, CELL_EMPTY, CELL_VALID):
               # log.debug("Flipping {},{}".format(r, c))
                self.set_cell(r, c, color)
                c += dx
                r += dy

    def in_game_field(self, row, col):
        return (row >= 0 and col >= 0 and row < self.game.size-1 and col < self.game.size-1)

    def is_valid_cell(self, row, col, color):
        """ is the cell valid for given user
        """
        if row < 0 or col < 0 or row > self.game.size-1 or col > self.game.size-1:
            # row, col outside
            return False

        if self.get_cell(row=row, col=col) != CELL_EMPTY:
            # not an empty cell
            return False

        # find enemy in neighbors cells
        for test_row, test_col in [(row-1, col-1), (row-1, col), (row-1, col+1),
                                   (row, col-1),                 (row, col+1),
                                   (row+1, col-1), (row+1, col), (row+1, col+1)]:
            if test_row < 0 or test_col < 0 or test_row > self.game.size-1 or test_col > self.game.size-1:
                #log.debug("{},{} outside".format(test_row, test_col))
                continue
            if self.get_cell(row=test_row, col=test_col) in (color, CELL_EMPTY):
                #log.debug("{},{} own tile or empty".format(test_row, test_col))
                continue

            # enemy tile found, now search for my own tile in this direction
            #log.debug("{},{} enemy".format(test_row, test_col))
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

                #log.debug("{},{} testing".format(test_row, test_col))
                if test_row < 0 or test_col < 0 or test_row > self.game.size-1 or test_col > self.game.size-1:
                    # outside
                    break

                #log.debug("{},{} is {}".format(test_row, test_col, self.get_cell(row=test_row, col=test_col)))
                if self.get_cell(row=test_row, col=test_col) == color:
                    # enemy tile found
                    return True
        return False

    def compute(self):
        """ calculate the next field state
        """
        pass

    def save(self, *args, **kwargs):
        if not self.field:
            # start constellation
            self.field = ",".join([CELL_EMPTY] * self.game.size**2)
            # place player1
            self.set_cell(row=(self.game.size/2)-1, col=(self.game.size/2)-1, tile=self.game.players.all()[0].color.name)
            self.set_cell(row=self.game.size/2, col=self.game.size/2, tile=self.game.players.all()[0].color.name)
            # place player2
            self.set_cell(row=(self.game.size/2)-1, col=self.game.size/2, tile=self.game.players.all()[1].color.name)
            self.set_cell(row=self.game.size/2, col=(self.game.size/2)-1, tile=self.game.players.all()[1].color.name)

        # calculate all field updates
        self.compute()

        # save
        super(Move, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0.pk} ({0.player.user.username} - {0.game})".format(self)


class Socket(models.Model):
    session = models.CharField(max_length=128)
    player = models.ForeignKey(Player, related_name="sockets")

    def __unicode__(self):
        return "{0.session} - {0.player.user.username}".format(self)
