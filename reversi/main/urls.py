from django.conf.urls import patterns, url

from .views import Index, About


urlpatterns = patterns(
    '',
    url(r'^$', Index.as_view(), name="index"),
    url(r'^about2$', About.as_view(), name="about"),
)
