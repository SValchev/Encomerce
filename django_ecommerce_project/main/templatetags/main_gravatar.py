from django import template
from urllib.parse import urlencode
import hashlib

register = template.Library()

HORDE_CHAR_DEFAULT = "http://img5.mmo.mmo4arab.com/news/2010/12/31/wow_avatar/wow_avatar_11.jpg"
ALLIANCE_CHAR_DEFAULT = "http://upload.qudong.com/uploads/allimg/110111/0Z10V221-1.jpg"

@register.simple_tag
def gavar_img(email,fraction ,alter=None, size=140):
    url = get_url(email,fraction ,size)
    alt = alter or ""
    result ="""<img alt="{}" src="{}" height={} width="{}">""".format(alt, url, size ,size)
    return result

@register.simple_tag
def get_url(email,fraction ,size=140):

    default = None

    if fraction == 'horde':
        default = HORDE_CHAR_DEFAULT
    elif fraction == 'alliance':
        default = ALLIANCE_CHAR_DEFAULT

    query_params = urlencode(
    [('s', str(size)),
     ('d', default)])

    return ("http://www.gravatar.com/avatar/"+
    hashlib.md5(email.lower().encode('utf-8')).hexdigest() +
    '?' +
     query_params)
