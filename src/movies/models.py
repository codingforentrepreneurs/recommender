import datetime
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q, F, Sum, Case, When
from django.db.models.signals import post_save, post_delete
from django.utils import timezone


from ratings.models import Rating

from . import tasks as movies_tasks

RATING_CALC_TIME_IN_DAYS = 3

class MovieQuerySet(models.QuerySet):
    def popular(self, reverse=False):
        ordering = '-score'
        if reverse:
            ordering = 'score'
        return self.order_by(ordering)
    
    def popular_calc(self, reverse=False):
        ordering = '-score'
        if reverse:
            ordering = 'score'
        return self.annotate(score=Sum(
                F('rating_avg') * F('rating_count'),
                output_field=models.FloatField()
            )
        ).order_by(ordering)

    def needs_updating(self):
        now = timezone.now()
        days_ago = now - datetime.timedelta(days=RATING_CALC_TIME_IN_DAYS)
        return self.filter(
            Q(rating_last_updated__isnull=True)|
            Q(rating_last_updated__lte=days_ago)
        )

class MovieManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return MovieQuerySet(self.model, using=self._db)

    def by_id_order(self, movie_pks=[]):
        qs = self.get_queryset().filter(pk__in=movie_pks)
        maintain_order = Case(*[When(pk=pki, then=idx) for idx, pki in enumerate(movie_pks)])
        return qs.order_by(maintain_order)
    
    def needs_updating(self):
        return self.get_queryset().needs_updating()

class Movie(models.Model):
    title = models.CharField(max_length=120, unique=True)
    overview = models.TextField()
    release_date = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating) # queryset
    rating_last_updated = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    rating_avg = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True) # 5.00, 0.00
    score = models.FloatField(blank=True, null=True)
    idx = models.IntegerField(help_text='Position IDs for ML', blank=True, null=True)

    objects = MovieManager()

    def get_absolute_url(self):
        return f"/movies/{self.id}/"

    def __str__(self):
        if not self.release_date:
            return f"{self.title}"
        return f"{self.title} ({self.release_date.year})"

    # def rating_avg_display(self):
    #     now = timezone.now()
    #     if not self.rating_last_updated:
    #         return self.calculate_rating()
    #     if self.rating_last_updated > now - datetime.timedelta(days=RATING_CALC_TIME_IN_DAYS):
    #         return self.rating_avg
    #     return self.calculate_rating()

    # def calculate_ratings_count(self):
    #     return self.ratings.all().count()
    
    # def calculate_ratings_avg(self):
    #     return self.ratings.all().avg()

    # def calculate_rating(self, save=True):
    #     rating_avg = self.calculate_ratings_avg()
    #     rating_count = self.calculate_ratings_count()
    #     self.rating_count= rating_count
    #     self.rating_avg = rating_avg
    #     self.rating_last_updated = timezone.now()
    #     if save:
    #         self.save()
    #     return self.rating_avg



def movie_post_save(sender, instance, created, *args, **kwargs):
    if created and instance.id:
        movies_tasks.update_movie_position_embedding_idx()

post_save.connect(movie_post_save, sender=Movie)

def movie_post_delete(*args, **kwargs):
    movies_tasks.update_movie_position_embedding_idx()


post_delete.connect(movie_post_delete, sender=Movie)