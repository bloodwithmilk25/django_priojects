from django import template
import re

register = template.Library()

url_re = re.compile(r"https?://(www\.)?")


@register.filter(name='strip_url')
def strip_url(val):
    return url_re.sub('', val).strip().strip('/')[:35]
