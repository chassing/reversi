from django.conf.urls import patterns, url, include

from .views import IndexView, UserProfileView, UserStatsView
from .views import GameView, NewGameView, ListGamesView, DenyGameView
from .views import HelpView

import socketio.sdjango
socketio.sdjango.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^socket\.io', include(socketio.sdjango.urls)),
    url(r'^user$', UserProfileView.as_view(), name="user-profile"),
    url(r'^stats$', UserStatsView.as_view(), name="user-stats"),
    url(r'^game/deny/(?P<id>\d+)$', DenyGameView.as_view(), name="deny-game"),
    url(r'^game/new/(?P<enemy>\d+)$', NewGameView.as_view(), name="new-game"),
    url(r'^game/(?P<id>\d+)$', GameView.as_view(), name="game"),
    url(r'^games$', ListGamesView.as_view(), name="list-games"),
    url(r'^help$', HelpView.as_view(), name="help"),
    url(r'^$', IndexView.as_view(), name="index"),
)
