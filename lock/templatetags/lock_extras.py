from django import template
register = template.Library()

def subtract(value, arg):
    return value - arg
register.filter('subtract', subtract)


def to_int(value):
    return int(value)

register.filter('to_int',to_int)
