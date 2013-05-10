from django.conf.urls import patterns, include, url
from django.contrib import admin

from registration.backends.default.views import RegistrationView
from main.forms import RegistrationForm

admin.autodiscover()

handler404 = 'site_basics.views.page_404'
handler500 = 'site_basics.views.page_500'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationForm)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('site_basics.urls')),
    url(r'^', include("main.urls", namespace="main")),
)
