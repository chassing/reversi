# Create your views here.

from django.template import RequestContext
from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = "main/index.html"

    def get(self, request):
        tmpl = RequestContext(request)
        tmpl["var1"] = "Hello World"
        return self.render_to_response(tmpl)


class About(TemplateView):
    template_name = "main/about.html"
