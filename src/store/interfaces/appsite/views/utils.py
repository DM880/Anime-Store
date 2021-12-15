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
        rating = round(avg_rating/counter)

    data_rating = {
        'rating': rating,
        'counter':counter
        }

    return data_rating


def pagination(page, obj_items):
    paginator = Paginator(obj_items, 4)

    try:
        all_items = paginator.page(page)
    except PageNotAnInteger:
        all_items = paginator.page(1)
    except EmptyPage:
        all_items = paginator.page(paginator.num_pages)

    return all_items


def get_session_key(request):

    if not request.session.session_key:
        request.session.create()
        session_key = request.session.session_key
    else:
        session_key = request.session.session_key

    return session_key