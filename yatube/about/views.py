from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """ Шаблон раздела 'Об Авторе' """

    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """ Шаблон раздела 'Технологии' """

    template_name = 'about/tech.html'
