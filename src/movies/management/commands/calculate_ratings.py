from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ratings.tasks import task_update_movie_ratings
# from movies.tasks import task_calculate_movie_ratings

User = get_user_model()

class Command(BaseCommand):    
    def handle(self, *args, **options):
        task_update_movie_ratings()