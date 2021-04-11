import base64
from django import template
from django.template.defaultfilters import stringfilter
import markdown as md

register = template.Library()
@register.filter(name='bin_2_img')
@stringfilter
def bin_2_img(img):
    if img is not None: return img.split(',')[-1] #[2:-1]

@register.filter(name='markdown')
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])