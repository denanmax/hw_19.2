from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def split(text):
    """Обрезает переданный текст до 100 символов"""
    result = text[0:100]
    return mark_safe(result)


@register.filter
def mediapath_filter(path):
    """Фильтр, который преобразует переданный путь в полный путь для доступа к медиафайлу"""
    return f"/media/{path}"


@register.simple_tag
def mymedia(val):
    if val:
        return f'/media/{val}'

    return '/media/no_photo.png'