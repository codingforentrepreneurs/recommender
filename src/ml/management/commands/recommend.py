from django.core.management.base import BaseCommand

from ml import tasks as ml_tasks

class Command(BaseCommand):
    help = "Train an iteration of your surprise recommnder model"
    
    def add_arguments(self, parser):
        parser.add_argument("--async", action='store_true', default=False)
        parser.add_argument("--offset", default=50, type=int)
        parser.add_argument("--max_pages", default=1_000, type=int)
        parser.add_argument("--users", default=[], type=list)

    def handle(self, *args, **options):
        is_async = options.get("async")
        offset = options.get('offset') or 50
        max_pages = options.get('max_pages') or 1_000
        users = options.get("users") or []
        users_ids = [x for x in users if x.isdigit()]
        kwargs = {
            "offset": offset,
            "max_pages": max_pages,
            "users_ids": users_ids
        }
        if is_async:
            ml_tasks.batch_users_prediction_task.apply_async(kwargs=kwargs)
        else:
            ml_tasks.batch_users_prediction_task(**kwargs)
        