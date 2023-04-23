from persistence.sql_app.models import Restaurant


def get_restaurant_review_rate(restaurant: Restaurant):
    avg_rating = 0
    reviews = restaurant.reviews
    for review in reviews:
        avg_rating += int(review.rating)
    if len(reviews) != 0:
        avg_rating = avg_rating / len(reviews)
    return avg_rating
