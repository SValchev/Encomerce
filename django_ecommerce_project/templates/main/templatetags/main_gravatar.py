from django import template
from urllib import urlencode
import hashlib

register = template.Library()

@register.simple_tag
def gavar_img(email, size=140):
    url = get_url(email, size)
    result =    """<img alt="" src="{}">""".format(url)

def get_url(email, size=140):

    default = ("http://img5.mmo.mmo4arab.com/news/2010/12/31/wow_avatar/wow_avatar_11.jpg")

    query_params = urlencode(
    [('s', str(size)),
     ('d', default)])

    return ("https://gravatar.com/avatar"+hashlib.md5(email.lower().encode('utf-8')).hexdigest() + '?' + query_params)
