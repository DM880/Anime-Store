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
