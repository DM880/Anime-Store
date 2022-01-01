from store.data.item.models import Item


def search_and_sort(items_category, searched_item, sorting_element):

    if items_category is not None and searched_item is not None:
        items = Item.objects.filter(
            category=items_category, name__contains=searched_item
        ).order_by(sorting_element)
    elif items_category is None and searched_item is not None:
        items = Item.objects.filter(name__contains=searched_item).order_by(
            sorting_element
        )
    elif items_category is not None and searched_item is None:
        items = Item.objects.filter(category=items_category).order_by(sorting_element)
    else:
        items = Item.objects.all().order_by(sorting_element)

    return items
