from django import template

register = template.Library()

@register.filter(name='bool_in_pl')
def bool_in_pl(value):
    "Convert True/False to Yes/No in Polish"
    return "Tak" if value else "Nie"