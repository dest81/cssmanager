from django import template
from django.conf import settings
import os


register = template.Library()

url=settings.STATIC_URL

URL_CSS=os.path.join(settings.STATIC_URL,'css/cssmanager.css')
URL_JS=os.path.join(settings.STATIC_URL,'js/cssmanager.js')
URL_PAN=os.path.join(settings.STATIC_URL,'js/jquery.tabslideout.v1.2.js')
URL_JS_CP=os.path.join(settings.STATIC_URL,'js/colorpicker.js')
URL_CSS_CP=os.path.join(settings.STATIC_URL,'css/colorpicker.css')

@register.simple_tag
def cssmanager_css():
    return '<link href="%s" rel="stylesheet" media="screen">' % URL_CSS



@register.simple_tag
def cssmanager_js():
    return '<link href="%s" rel="stylesheet" media="screen"> \n <script src="%s"></script>' \
           ' \n <script src="%s"></script> \n <script src="%s"></script>' %  (URL_CSS_CP,URL_JS,URL_PAN,URL_JS_CP)

