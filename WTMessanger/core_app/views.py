from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class CoreView(TemplateView):
    template_name = "core.html"

class MyPublicationsView(TemplateView):
    template_name = "my_publications.html"