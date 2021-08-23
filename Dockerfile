FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD python3 manage.py runserver 0.0.0.0:8000
