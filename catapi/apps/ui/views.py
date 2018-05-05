from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = 'index.html'


class BreedsView(TemplateView):

    template_name = 'breeds.html'


class SpecsView(TemplateView):

    template_name = 'specs.html'
