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

        try:
            last_move = self.last_move()
        except IndexError:
            return player1

        # who is the next player
        next = player2 if last_move.player == player1 else player1
        return next
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
    game = models.ForeignKey(Game)
    date = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        ordering = ('date',)

    def grid(self):
        """ get grid representation

        [
          [XXX,XXX,XXX, ... ,XXX]
          ...
          [XXX,XXX,XXX, ... ,XXX]
        ]
        """
        def _get_row(row_nr, move):
            row = []
            for col_nr, state in enumerate(move):
                row.append({
                    "state": state,
                    "row": row_nr,
                    "col": col_nr,
                })
            return row

        grid = []
        for row in xrange(0, self.game.size):
            grid.append(_get_row(row, self.field.split(",")[row*self.game.size:row*self.game.size+self.game.size]))
        return grid

    def set_cell(self, row, col, tile):
        """ place a 'tile'
        """
        field_list = list(self.field.split(","))
        log.debug(field_list)
        log.debug(row*self.game.size+col)
        field_list[row*self.game.size+col] = tile
        self.field = ",".join(field_list)

    def get_cell(self, row, col):
        """ return 'tile' on select place
        """
        return self.field.split(",")[row*self.game.size+col]

    def save(self, *args, **kwargs):
        if not self.field:
            # compute start constallation
            self.field = ",".join([CELL_EMPTY] * self.game.size**2)
            # place player1
            self.set_cell(row=(self.game.size/2)-1, col=(self.game.size/2)-1, tile=self.game.players.all()[0].color.name)
            self.set_cell(row=self.game.size/2, col=self.game.size/2, tile=self.game.players.all()[0].color.name)
            # place player2
            self.set_cell(row=(self.game.size/2)-1, col=self.game.size/2, tile=self.game.players.all()[1].color.name)
            self.set_cell(row=self.game.size/2, col=(self.game.size/2)-1, tile=self.game.players.all()[1].color.name)

        super(Move, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0.field} ({0.player.user.username} - {0.game})".format(self)


class Socket(models.Model):
    session = models.CharField(max_length=128)
    player = models.ForeignKey(Player, related_name="sockets")

    def __unicode__(self):
        return "{0.session} - {0.player.user.username}".format(self)
