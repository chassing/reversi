from django.db import models
from django.contrib.auth.models import AbstractUser


class ReversiUser(AbstractUser):
    nickname = models.CharField(max_length=254)


class TileColor(models.Model):
    name = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class Game(models.Model):
    players = models.ManyToManyField(ReversiUser, through='Player')

    def __unicode__(self):
        return "{0.pk} - {1}".format(self, self.players.all())


class Player(models.Model):
    user = models.ForeignKey(ReversiUser)
    game = models.ForeignKey(Game)
    color = models.ForeignKey(TileColor)

    def __unicode__(self):
        return "{0.user.username} - {0.game} - {0.color}".format(self)


class Socket(models.Model):
    session = models.CharField(max_length=128)
    player = models.ForeignKey(Player, related_name="sockets")

    def __unicode__(self):
        return "{0.session} - {0.player.user.username}".format(self)
