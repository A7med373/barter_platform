from django.middleware.csrf import get_token
from django.urls import reverse
from django.templatetags.static import static
from django.template.defaultfilters import truncatewords, date as django_date
from django.contrib.auth.context_processors import auth
from jinja2 import Environment
from markupsafe import Markup
from apps.ads.templatetags.ads_extras import status_color
from datetime import datetime

def jinja_url(viewname, *args, **kwargs):
    """
    Поддерживает как позиционные, так и именованные аргументы
    """
    if kwargs:
        return reverse(viewname, kwargs=kwargs)
    return reverse(viewname, args=args)


def strftime_filter(value, format_string):
    """
    Фильтр для форматирования даты в Jinja2
    """
    if isinstance(value, datetime):
        return value.strftime(format_string)
    return value


def environment(**options):
    env = Environment(**options)

    # Добавляем контекстные процессоры Django
    def get_context(request):
        context = {}
        context.update(auth(request))
        return context

    env.globals.update({
        "url": jinja_url,
        "static": static,
        "get_context": get_context,

        # <input type="hidden" …> — безопасная строка
        "csrf_field": lambda req: Markup(
            f'<input type="hidden" name="csrfmiddlewaretoken" '
            f'value="{get_token(req)}">'
        ),
    })

    # регистрируем фильтры
    env.filters["truncatewords"] = lambda s, num=20: truncatewords(s, num)
    env.filters['status_color'] = status_color
    env.filters['date'] = django_date
    env.filters['strftime'] = strftime_filter

    return env