from django import template

register = template.Library()

@register.filter
def hash(dictionary, key):
    return dictionary.get(key)

@register.filter
def index(list_ids, key):
    key = int(key)
    return list_ids[key]