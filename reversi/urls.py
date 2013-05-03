from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin


admin.autodiscover()

handler404 = 'site_basics.views.page_404'
handler500 = 'site_basics.views.page_500'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    # redirect old login link
    url(r'^accounts/login.*$', RedirectView.as_view(url="/")),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('site_basics.urls')),
    url(r'^', include("main.urls", namespace="main")),
)
