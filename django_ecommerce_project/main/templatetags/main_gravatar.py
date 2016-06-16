from django import template
from urllib.parse import urlencode
import hashlib

register = template.Library()

@register.simple_tag
def gavar_img(email, alter=None, size=140):
    url = get_url(email, size)
    alt = alter or ""
    result ="""<img alt="{}" src="{}" height={} width="{}">""".format(alt, url, size ,size)
    return result

@register.simple_tag
def get_url(email, size=140):

    default = ("http://img5.mmo.mmo4arab.com/news/2010/12/31/wow_avatar/wow_avatar_11.jpg")

    query_params = urlencode(
    [('s', str(size)),
     ('d', default)])

    return ("http://www.gravatar.com/avatar/"+
    hashlib.md5(email.lower().encode('utf-8')).hexdigest() +
    '?' +
     query_params)
