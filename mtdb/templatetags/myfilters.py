from django import template
from django.contrib.auth.models import User
from ..models import Like, Review

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='get_by_index')
def get_by_index(sequence, position):
    return sequence[position]

@register.filter(name='qs_gMap')
def qs_gMap(value):
    return value.replace(' ', '+')

@register.simple_tag
def has_liked(user_id, review_id):
    if Like.objects.filter(user=User.objects.get(id=user_id), review=Review.objects.get(id=review_id)).exists():
        return True
    return False