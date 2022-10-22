FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBEFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app
COPY . /usr/local/bin/entrypoint.sh
RUN chmod /usr/local/bin/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

CMD ["gunicorn", "-b", "0.0.0.0:8000", "config.wsgi:application"]
