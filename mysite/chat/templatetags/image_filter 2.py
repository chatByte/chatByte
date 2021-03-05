import base64
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter(name='bin_2_img')
@stringfilter
def bin_2_img(img):
    print(img[1:-1])
    print(type(img))
    if img is not None: return img[2:-1]