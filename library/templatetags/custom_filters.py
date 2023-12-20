from django import template

register = template.Library()

@register.filter(name='stars')
def stars(value):
    full_stars = int(value)
    half_star = 1 if value - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return {
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
    }
