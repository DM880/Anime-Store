from django.core.paginator import Paginator


def rating_avg(reviews):

    avg_rating = 0
    counter = 0

    for review in reviews:
        avg_rating += review.rating
        counter += 1

    if avg_rating == 0:
        rating = 0
    else:
        rating = round(avg_rating / counter)

    data_rating = {"rating": rating, "counter": counter}

    return data_rating


def pagination(page, obj_items, page_range):
    paginator = Paginator(obj_items, page_range)

    try:
        all_items = paginator.page(page)
    except PageNotAnInteger:
        all_items = paginator.page(1)
    except EmptyPage:
        all_items = paginator.page(paginator.num_pages)

    return all_items

