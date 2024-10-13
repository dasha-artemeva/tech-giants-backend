from typing import Iterable

from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ComponentDecorator:
    def __init__(self): ...

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            if callable(getattr(f, "prepare_args", None)):
                args, kwargs = f.prepare_args(*args, **kwargs)
            return format_html(f.__doc__, *args, **kwargs)

        return wrapper

    def join(self, components: Iterable):
        return mark_safe("\n".join(components))


component = ComponentDecorator()
