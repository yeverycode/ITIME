from django import template

register = template.Library()

@register.filter(name='to_int')
def to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0  # 또는 원하는 기본값

