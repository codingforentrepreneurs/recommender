from django.core.management.base import BaseCommand

from ml import tasks as ml_tasks

class Command(BaseCommand):
    help = "Train an iteration of your surprise recommnder model"
    
    def add_arguments(self, parser):
        parser.add_argument("--async", action='store_true', default=False)
        parser.add_argument("--epochs", default=20, type=int)

    def handle(self, *args, **options):
        is_async = options.get("async")
        n_epochs = options.get('epochs') or 20
        kwargs = {"n_epochs": n_epochs}
        if is_async:
            ml_tasks.train_surprise_model_task.apply_async(kwargs=kwargs)
        else:
            ml_tasks.train_surprise_model_task(**kwargs)
        