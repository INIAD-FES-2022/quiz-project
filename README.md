# Quiz application for Akabanedai-Fes
This is a web application for holding quizzes programs.

# Requirements
* PostgreSQL
* redis
* nginx (or web server which is compatible with WebSocket)
Environments under Docker is tested.

# Installation
## For production
1. Clone this repository.
2. Make ".env" file.(see [Config](#Config))
3. Run `docker-compose -f docker-compose-prd.yml up -d`

You'll need to run `python manage.py createsuperuser` to create a superuser.

## For development
1. Clone this repository.
2. Make ".env" file.(see [Config](#Config))
3. Run `python daphne/manage.py migrate`
4. Run `python daphne/manage.py runserver`

You'll need to run `python manage.py createsuperuser` to create a superuser. 

# Config
```.env
# DEBUG=True
DEBUG=False

DJANGO_SECRET_KEY=SECRETKEY(replace here)
CSRF_TRUSTED_ORIGINS=https://your-website-origin, # Don't forget comma
ALLOWED_HOSTS=your-website-origin, # Don't forget comma 

# IS_POSTGRES=False to use SQLite
IS_POSTGRES=True
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
# If you use Docker to run DB, set POSTGRES_HOST=db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# If you need to use S3 to store static files, enter values below
USE_S3=True
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=

MEDIA_ROOT=/var/lib/media/
STATIC_ROOT=/var/lib/static/
APP_ROOT=/usr/src/app

# If you use Docker to run Redis, set REDIS_HOST=redis
REDIS_HOST=redis
REDIS_PORT=6379 

# If you use Docker to run nginx, set SERVER_NAME
SERVER_NAME=

# If you use Docker to get certification from Let's encrypt using certbot, enter a value below to get notification for update the certification
EMAIL_ADDRESS=
```
