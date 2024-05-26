FROM python:3.10

ENV PYTHONUNBUFFERED 1

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV}

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
