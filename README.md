# Quiz application for Akabanedai-Fes
This is a web application for holding quizzes programs.

# Requirements
* PostgreSQL
* redis
* nginx (or web server which is compatible with WebSocket)
Environments under Docker is tested.

# Installation
1. Clone this repository.
2. Make ".env" file.(see [Config](#Config))
3. Run `docker-compose up -d`

# Config
```.env
# DEBUG=True
DEBUG=False

DJANGO_SECRET_KEY=SECRETKEY(replace here)
CSRF_TRUSTED_ORIGINS=https://your-website-origin, # Don't forget comma
ALLOWED_HOSTS=your-website-origin, # Don't forget comma 

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# If you use S3 to store static files and want to read them from S3, enter values below
USE_S3=True
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

MEDIA_ROOT=/var/lib/media/
STATIC_ROOT=/var/lib/static/
APP_ROOT=/usr/src/app

REDIS_HOST=redis
REDIS_PORT=6379 
```
