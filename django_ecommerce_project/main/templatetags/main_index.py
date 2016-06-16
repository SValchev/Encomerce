from django import template
import hashlib

register = template.Library()

@register.simple_tag
def get_style(fraction):
    return """background: url("/static/img/{}-background.jpg");
    background-size: cover;
    height: 135px;""".format(fraction)
