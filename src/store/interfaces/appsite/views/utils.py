from store.data.item.models import Item, ItemReview


def rating_avg(reviews):

    avg_rating = 0
    counter = 0

    for review in reviews:
        avg_rating += review.rating
        counter += 1

    if avg_rating == 0:
        rating = 0
    else:
        rating = round(avg_rating/counter)

    data_rating = {
        'rating': rating,
        'counter':counter
        }

    return data_rating


def search_and_sort(items_category, searched_item, sorting_element):

    if items_category is not None and searched_item is not None:
        items = Item.objects.filter(category=items_category, name__contains=searched_item).order_by(sorting_element)
    elif items_category is None and searched_item is not None:
        items = Item.objects.filter(name__contains=searched_item).order_by(sorting_element)
    elif items_category is not None and searched_item is None:
        items = Item.objects.filter(category=items_category).order_by(sorting_element)
    else:
        items = Item.objects.all().order_by(sorting_element)

    return items


def get_session_key(request):

    if not request.session.session_key:
        request.session.create()
        session_key = request.session.session_key
    else:
        session_key = request.session.session_key

    return session_key