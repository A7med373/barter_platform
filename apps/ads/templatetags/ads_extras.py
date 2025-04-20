from django import template

register = template.Library()

@register.filter
def status_color(status):
    color_map = {
        'pending': 'secondary',
        'accepted': 'success',
        'declined': 'danger',
    }
    return color_map.get(status, 'secondary') 