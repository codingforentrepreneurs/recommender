

from .models import Movie


def task_calculate_movie_ratings(all=False, count=None):
    qs = Movie.objects.needs_updating()
    if all:
        qs = Movie.objects.all()
    qs = qs.order_by('rating_last_updated')
    if isinstance(count, int):
        qs = qs[:count]
    for obj in qs:
        obj.calculate_rating(save=True)