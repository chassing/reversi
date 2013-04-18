from django.contrib import admin

from .models import ReversiUser
from .models import Player
from .models import Game
from .models import Move
from .models import TileColor
from .models import Socket


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1


class ReversiUserAdmin(admin.ModelAdmin):
    inlines = (PlayerInline,)


class GameModelAdmin(admin.ModelAdmin):
    inlines = (PlayerInline,)


admin.site.register(ReversiUser, ReversiUserAdmin)
admin.site.register(Player)
admin.site.register(Game, GameModelAdmin)
admin.site.register(Move)
admin.site.register(TileColor)
admin.site.register(Socket)
