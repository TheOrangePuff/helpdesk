FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

WORKDIR /code

CMD python3 manage.py runserver 0.0.0.0:8000
