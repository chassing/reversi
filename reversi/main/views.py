# Create your views here.

from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from .models import Game


class IndexView(TemplateView):
    template_name = "main/index.html"

    @method_decorator(login_required)
    def get(self, request):
        tmpl = RequestContext(request)
        tmpl["games"] = Game.objects.filter(players=self.request.user)
        return self.render_to_response(tmpl)


class GameView(TemplateView):
    template_name = "main/game.html"

    @method_decorator(login_required)
    def get(self, request, id):
        tmpl = RequestContext(request)
        tmpl["game"] = get_object_or_404(Game, pk=id)
        tmpl["user"] = request.user
        tmpl["field_size"] = xrange(0, 8)
        return self.render_to_response(tmpl)


class NewGameView(TemplateView):
    template_name = "main/new-game.html"

    @method_decorator(login_required)
    def get(self, request):
        tmpl = RequestContext(request)
        # todo game form
        return self.render_to_response(tmpl)


class AboutView(TemplateView):
    template_name = "main/about.html"
