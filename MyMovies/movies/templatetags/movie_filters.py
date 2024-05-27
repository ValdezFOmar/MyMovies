from django import template

register = template.Library()


@register.filter(is_safe=True)
def movie_duration(duration_in_minutes: int) -> str:
    hours, minutes = divmod(duration_in_minutes, 60)
    h = f'{hours}h' if hours else ''
    m = f'{minutes}min' if minutes else ''
    sep = ' ' if hours and minutes else ''
    return h + sep + m
