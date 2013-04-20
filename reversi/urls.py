from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'site_basics.views.page_404'
handler500 = 'site_basics.views.page_500'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),
    url(r'^', include('site_basics.urls')),
    url(r'^', include("main.urls", namespace="main")),
)
