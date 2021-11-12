def rating_avg(reviews):

    avg_rating = 0
    counter = 0

    for review in reviews:
        avg_rating += review.rating
        counter += 1

    data_rating = {
        'rating':round(avg_rating/counter),
        'counter':counter
        }

    return data_rating
