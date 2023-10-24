# Course work №7 - "Tracker of userful habits".
# The project using Django DRF framework.


## Description
The "REST API service" of the userful habits tracker SPA application is implemented.
Allows users to register on the service and post new useful habits,
with a reminder of their fulfillment via a telegram bot.

## Requirements
- python = "^3.11"
- django = "^4.2.6"
- psycopg2-binary = "^2.9.9"
- pillow = "^10.1.0"
- python-dotenv = "^1.0.0"
- djangorestframework = "^3.14.0"
- django-filter = "^23.3"
- djangorestframework-simplejwt = "^5.3.0"
- coverage = "^7.3.2"
- drf-yasg = "^1.21.7"
- django-cors-headers = "^4.3.0"
- celery = "^5.3.4"
- redis = "^5.0.1"
- django-celery-beat = "^2.5.0"
- requests = "^2.31.0"

## Set Up your settings
Create a .env configuration file with your personal settings in the root of the project,
according to the sample, specified in .env.sample.
Fill out the file according to your personal data.

## Prepare the start of the project
- Run the Redis service
- Create a database in postgresql.
  (the name of the database must match the name specified in the file)
- Migrate your database using following commands:
    * python3 manage.py makemigrations
    * python3 manage.py migrate
- Create the superuser:
    * python3 manage.py csu
- Create a telegram bot for send notifications to users and write your token into the .env file

To run the project, enter following commands in the terminal windows:
- python3 manage.py runserver
- celery -A config worker -l INFO -c 1
- celery -A config beat -l info -S django 

## The main working links
- To read an API documentation follow the next link: http://127.0.0.1:8000/redoc/
- To log in to the admin panel, follow this link: http://127.0.0.1:8000/admin/