from django.shortcuts import render
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['test_top_products'] = range(4)
        return context

class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О магазине'
        return context

class ProjectView(TemplateView):
    template_name = "main/project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте'
        return context

def page_not_found(request, exception):
    return render(request, "404.html", status=404)

def server_error(request):
    return render(request, "error.html", status=500)