
from django import template

from urllib.parse import urlencode


register = template.Library()


@register.filter(name="split_paragraphs")
def split_paragraphs(value):
    if not value:
        return []

    text = str(value).replace("\r\n", "\n").replace("\r", "\n")

    paragraphs = []
    for p in text.split("\n\n"):
        p = p.strip()
        if not p:
            continue
        paragraphs.append(p.replace("\n", "<br>"))

    return paragraphs


@register.simple_tag(takes_context=True)
def update_query(context, **kwargs):
    request = context.get("request")
    if not request:
        return urlencode(kwargs)

    query = request.GET.copy()
    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()
