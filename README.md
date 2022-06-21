# feeder
Scraping submitted rss feeds and update news.

# usage
To run the project, use `docker-compose up --build`.<br>
Also you can create `.env` file from `.example.env` and use in docker-compose.<br>

Celery task runs every hour. If any Exception happened, it retries in exponentially pattern for 5 times.
