from django import template
from datetime import datetime
register = template.Library()


@register.filter(name="time_converter")
def time_converter(value):

    return '{:2d}h {:2d}m'.format(*divmod(value, 60))
