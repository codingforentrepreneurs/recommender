[![Recommender Course Image](https://static.codingforentrepreneurs.com/media/courses/recommender/8aa6d83c-8134-4e68-8954-65bc978033b2.jpg)](https://www.codingforentrepreneurs.com/courses/recommender/)

# Recommender

Build a recommendation engine using Django &amp; a Machine Learning technique called Collaborative Filtering.

[Live demo with limited features](http://recommender.demo.cfe.sh)

## Getting Started

1. Clone the project and make it your own. Use branch `start` initially so we can all start in the same place.
```bash
git clone https://github.com/codingforentrepreneurs/recommender
cd recommender
```
If you're _starting in the course_, use the following:

```
git checkout start
rm -rf .git
git init .
git add --all
git commit -m "My recommender project"
```

2. Create virtual environment and activate it.

```bash
python3.8 -m venv venv
source venv/bin/activate
```
Use `.\venv\Scripts\activate` if on windows

3. Install requirements
```
(venv) python -m pip install pip --upgrade
(venv) python -m pip install -r requirements.txt
```

4. Open VSCode
```bash
code .
```

5. Create `.env` file:

In `src/.env` add:
```
CELERY_BROKER_REDIS_URL='redis://localhost:6380'
DJANGO_DEBUG='1'
SECRET_KEY='o43ig(nx@1)ae$y6_@lbh95fp@3#lda3!y6agi&r3e+m-z$cu_'
```
Replace your `SECRET_KEY` with a new one using [this guide](https://www.codingforentrepreneurs.com/blog/create-a-one-off-django-secret-key/) or simply:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

6. Start Docker Compose for a Redis Instance

Below will start a docker-based Redis instance that will run at port 6380 on your local machine to match the `.env` from the previous step.
```
docker compose up -d
```
Consider watching my [Docker & Docker Compose](https://www.codingforentrepreneurs.com/courses/docker-and-docker-compose/) course if you're new to docker.

7. Run Django Commands

```
cd path/to/recommender
source venv/bin/activate
$(venv) cd src
```

Migrations and Create Superuser
```
$(venv) python manage.py makemigrations
$(venv) python manage.py migrate
$(venv) python manage.py createsuperuser
```

Run the server:
```
$(venv) python manage.py runserver
```

8. Download the Movies Dataset
- Go to [this kaggle project](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
- Login or sign up
- Download [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
- Expand archive.zip (the downloaded file)
- Copy contents into `recommender/src/data` so that you have:

```
# in recommender projectdir
$(venv) ls src/data
credits.csv             links.csv               movies_metadata.csv     ratings_small.csv
keywords.csv            links_small.csv         ratings.csv
```
We only need `links_small.csv`, `ratings_small.csv`, and `movies_metadata.csv` at this time.

The entire `src/data` folder is in `.gitignore` so you do not accidently commit this data to your git repo.

9. Load in Movie Data
Run migrations if needed:
```
python manage.py makemigrations
python manage.py migrate
```
Then:
```
python manage.py loader 200_000 --movies
```

10. Load in Rating Data 
```
python manage.py dataset_ratings
```

11. Train your ML Model
```
python manage.py train --epochs 20
```
When your worker is running, you can also do `python manage.py train --async --epochs 20`

12. Run the Worker
```
celery -A cfehome worker -l info --beat
```

13. Rate some movies
With the server running (`python manage.py runserver`) open up [http://localhost:8000/accounts/login](http://localhost:8000/login) and rate some movies.

14. Create recommendation predictions

```
python manage.py recommend
```
> This can also be done as a periodic task

15. Review Predictions on Dashboard

16. Celebrate!

## Helpful Guides
- [Using a Cloud-based Redis Server](https://www.codingforentrepreneurs.com/blog/remote-redis-servers-for-development/)
- [Install Redis on Windows](https://www.codingforentrepreneurs.com/blog/redis-on-windows/)
- [Install Redis on macOS](https://www.codingforentrepreneurs.com/blog/install-redis-mac-and-linux)
- [Celery + Redis + Django Setup Guide](https://www.codingforentrepreneurs.com/blog/celery-redis-django/)
