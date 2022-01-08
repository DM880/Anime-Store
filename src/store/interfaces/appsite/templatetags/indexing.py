from django import template

register = template.Library()

@register.filter
def hash(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def index(index_count, order_count):

    index_count = int(index_count)

    counter = int(order_count[index_count])
    print(counter)

    return counter

