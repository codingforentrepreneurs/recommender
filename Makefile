build:
	docker build -t recommender -f Dockerfile . 

run:
	docker run --env-file ./src/.env -p 8200:80 --name recommender --rm  recommender

stop:
	docker stop recommender

push:
	docker build --platform=linux/amd64 -t codingforentrepreneurs/recommender:latest -f Dockerfile . 
	docker push codingforentrepreneurs/recommender --all-tags

runserver:
	cd src && ../venv/bin/python manage.py runserver

requirements:
	venv/bin/pip-compile --output-file src/requirements.txt --upgrade src/requirements/requirements.in
	venv/bin/python -m pip install -r src/requirements.txt
