from django import template
from datetime import datetime
register = template.Library()


@register.filter(name="time_converter")
def time_converter(value):

    return '{:2d}h {:2d}m'.format(*divmod(value, 60))

# def time_converter(value):
#     return '{:2d}h {:2d}m'.format(*divmod(value, 60))

# register = template.Library()
# register.filter('time_converter', time_converter)