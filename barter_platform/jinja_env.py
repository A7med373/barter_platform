from django.middleware.csrf import get_token
from django.urls import reverse
from django.templatetags.static import static
from django.template.defaultfilters import truncatewords
from jinja2 import Environment
from markupsafe import Markup

def jinja_url(viewname, *args, **kwargs):
    """
    Поддерживает как позиционные, так и именованные аргументы
    """
    if kwargs:
        return reverse(viewname, kwargs=kwargs)
    return reverse(viewname, args=args)


def environment(**options):
    env = Environment(**options)

    env.globals.update({
        "url": jinja_url,
        "static": static,

        # <input type="hidden" …> — безопасная строка
        "csrf_field": lambda req: Markup(
            f'<input type="hidden" name="csrfmiddlewaretoken" '
            f'value="{get_token(req)}">'
        ),
    })

    # регистрируем фильтр  truncatewords
    env.filters["truncatewords"] = lambda s, num=20: truncatewords(s, num)

    return env