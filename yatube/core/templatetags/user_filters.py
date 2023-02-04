from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """ CSS фильтр """
    return field.as_widget(attrs={'class': css})
