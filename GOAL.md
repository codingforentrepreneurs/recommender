Django as a Machine Learning Pipeline Orchestration Tool:
    - Get Data - via Django
        - [x] User
        - [] Ratings -> Collaborative Filtering
        - [x] Dataset -> Movies
            - Scrape from the Internet
            - API -> Software-to-software
            - User-generated content -> cold start problem
            - [x] Open Source Datasets -> Kaggle -> The Movies Dataset
    - Prepare Data - via Django & Pandas
    - Train Model from Data - via Django & Celery using Keras
    - Use Model on New Data - via Django & Celery using Keras

We're not solving cold start problem, we're solving the ML pipeline orchestration problem