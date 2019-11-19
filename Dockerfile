FROM python:3.7.5

WORKDIR /usr/src/app

RUN pip install djangorestframework

COPY . .

CMD [ "python3 manage.py runserver"]