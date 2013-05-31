# Create your views here.
from logging import getLogger
log = getLogger("main.views")

from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect

from registration.backends.default.views import RegistrationView as RegistrationViewOrig

from .models import ReversiUser
from .models import Game
from .models import Player, CELL_PLAYER1, CELL_PLAYER2

from .forms import MultiplayerGameForm
from .forms import ProfileForm
from .forms import RegistrationForm


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get(self, request):
        tmpl = RequestContext(request)
        if request.GET.get("q"):
            tmpl["users"] = ReversiUser.objects.filter(nickname__icontains=request.GET.get("q")).order_by("nickname")
        else:
            tmpl["users"] = ReversiUser.objects.all().order_by("nickname")
        return self.render_to_response(tmpl)


class GameView(TemplateView):
    template_name = "main/game.html"

    @method_decorator(login_required)
    def get(self, request, id):
        tmpl = RequestContext(request)
        tmpl["game"] = game = get_object_or_404(Game, pk=id)
        tmpl["player"] = get_object_or_404(Player, user=request.user, game=game)
        tmpl["field_size"] = xrange(0, 8)
        tmpl["use_angular"] = True
        return self.render_to_response(tmpl)


class NewGameView(TemplateView):
    template_name = "main/new-game.html"

    @method_decorator(login_required)
    def get(self, request, enemy, form=None):
        tmpl = RequestContext(request)
        if not form:
            tmpl["form"] = MultiplayerGameForm(user=request.user)
        else:
            tmpl["form"] = form
        return self.render_to_response(tmpl)

    @method_decorator(login_required)
    def post(self, request, enemy):
        form = MultiplayerGameForm(user=request.user, data=request.POST)
        if form.is_valid():
            game = Game(name=form.cleaned_data['name'])
            game.save()
            user2 = get_object_or_404(ReversiUser, pk=enemy)
            if form.cleaned_data['player'] == CELL_PLAYER1:
                # i'm player1
                player1 = request.user
                player2 = user2
                if form.cleaned_data['color'] == CELL_PLAYER1:
                    player1_color = CELL_PLAYER1
                    player2_color = CELL_PLAYER2
                else:
                    player1_color = CELL_PLAYER2
                    player2_color = CELL_PLAYER1
            else:
                # i'm player2
                player1 = user2
                player2 = request.user
                if form.cleaned_data['color'] == CELL_PLAYER1:
                    player1_color = CELL_PLAYER2
                    player2_color = CELL_PLAYER1
                else:
                    player1_color = CELL_PLAYER1
                    player2_color = CELL_PLAYER2

            Player.objects.create(
                game=game,
                user=player1,
                color=player1_color,
            )
            Player.objects.create(
                game=game,
                user=player2,
                color=player2_color,
            )
            return redirect("main:game", id=game.pk)
        return self.get(request, enemy, form)


class ListGamesView(TemplateView):
    template_name = "main/list-games.html"

    @method_decorator(login_required)
    def get(self, request):
        tmpl = RequestContext(request)
        tmpl["games"] = Game.objects.filter(players__user=request.user)
        tmpl["user"] = request.user
        return self.render_to_response(tmpl)


class DenyGameView(TemplateView):
    template_name = "main/deny-game.html"

    @method_decorator(login_required)
    def get(self, request, id):
        tmpl = RequestContext(request)
        tmpl["game"] = game = get_object_or_404(Game, pk=id)

        if request.GET.get("a") == "yes":
            # user denied this game
            player = get_object_or_404(Player, user=request.user, game=game)
            player.denied = True
            player.save()
            return redirect("main:list-games")
        return self.render_to_response(tmpl)


class UserProfileView(TemplateView):
    template_name = "main/user-profile.html"

    @method_decorator(login_required)
    def get(self, request, form=None):
        tmpl = RequestContext(request)
        if not form:
            tmpl["form"] = ProfileForm(instance=request.user)
        else:
            tmpl["form"] = form
        return self.render_to_response(tmpl)

    @method_decorator(login_required)
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = None
        return self.get(request, form)


class UserStatsView(TemplateView):
    template_name = "main/user-stats.html"

    @method_decorator(login_required)
    def get(self, request, form=None):
        tmpl = RequestContext(request)
        tmpl["user"] = request.user
        return self.render_to_response(tmpl)


class HelpView(TemplateView):
    template_name = "main/help.html"

    @method_decorator(login_required)
    def get(self, request, form=None):
        tmpl = RequestContext(request)
        return self.render_to_response(tmpl)


class RegistrationView(RegistrationViewOrig):
    form_class = RegistrationForm

    def register(self, request, **cleaned_data):
        new_user = super(RegistrationView, self).register(request, **cleaned_data)
        new_user.nickname = cleaned_data['nickname']
        new_user.save()
