import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')

app = Celery('cfehome')

# CELERY_
app.config_from_object("django.conf:settings", namespace='CELERY')

# app.conf.broker_url = ''
# app.conf.result_backend ='django-db'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "run_movie_rating_avg_every_30": {
        'task': 'task_update_movie_ratings',
        'schedule': 60 * 30, # 30 min,
    },
    "daily_movie_idx_refresh": {
        "task": "movies.tasks.update_movie_position_embedding_idx",
        "schedule": crontab(hour=1, minute=0)
    },
    "daily_rating_dataset_export": {
        "task": "export_rating_dataset",
        "schedule": crontab(hour=1, minute=30)
    },
    "daily_rating_dataset_export": {
        "task": "export_movies_dataset",
        "schedule": crontab(hour=2, minute=15)
    },
    "daily_train_surprise_model": {
        "task": "ml.tasks.train_surprise_model_task",
        "schedule": crontab(hour=3, minute=0)
    },
    "daily_model_inference": {
        "task": "ml.tasks.batch_users_prediction_task",
        "schedule": crontab(hour=4, minute=30),
        "kwargs": {"max_pages": 5000, "offset": 200}
    },
    
}