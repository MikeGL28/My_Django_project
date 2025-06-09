from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def addcss(field, css):
    return field.as_widget(attrs={"class": css})