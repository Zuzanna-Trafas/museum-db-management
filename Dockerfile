FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ENTRYPOINT rm -f ./*/migrations/0*.py &&\
#           python3 manage.py makemigrations &&\
           python3 manage.py migrate &&\
           python3 manage.py createsuperuser &&\
           python3 manage.py runserver 0.0.0.0:8000
