from django import template

register = template.Library()

@register.filter(name='is_image')
def is_image(file_name):
    return file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
