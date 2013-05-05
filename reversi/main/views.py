# Create your views here.
from logging import getLogger
log = getLogger("main.views")

from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect

from .models import Game
from .models import Player

from forms import MultiplayerGameForm
from forms import ProfileForm


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get(self, request):
        tmpl = RequestContext(request)
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
    def get(self, request, form=None):
        tmpl = RequestContext(request)
        if not form:
            tmpl["form"] = MultiplayerGameForm(request.user)
        else:
            tmpl["form"] = form
        return self.render_to_response(tmpl)

    @method_decorator(login_required)
    def post(self, request):
        form = MultiplayerGameForm(request.user, request.POST)
        if form.is_valid():
            game = Game(name=form.cleaned_data['name'])
            game.save()
            Player.objects.create(
                game=game,
                user=form.cleaned_data['player1'],
                color=form.cleaned_data['color_player1'],
            )
            Player.objects.create(
                game=game,
                user=form.cleaned_data['player2'],
                color=form.cleaned_data['color_player2'],
            )
            return redirect("main:game", id=game.pk)
        return self.get(request, form)


class ListGamesView(TemplateView):
    template_name = "main/list-games.html"

    @method_decorator(login_required)
    def get(self, request):
        tmpl = RequestContext(request)
        tmpl["games"] = Game.objects.filter(players__user=request.user)
        return self.render_to_response(tmpl)


class UserProfileView(TemplateView):
    template_name = "main/user-profile.html"

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
