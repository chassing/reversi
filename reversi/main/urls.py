from django.conf.urls import patterns, url, include

from .views import IndexView, AboutView
from .views import GameView

import socketio.sdjango
socketio.sdjango.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^socket\.io', include(socketio.sdjango.urls)),
    url(r'^about$', AboutView.as_view(), name="about"),
    url(r'^game/(?P<id>\d+)$', GameView.as_view(), name="game"),
    url(r'^$', IndexView.as_view(), name="index"),
)
