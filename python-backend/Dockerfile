FROM python:3-slim

COPY requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt

RUN mkdir /tmp/images

COPY . /api
WORKDIR /api
COPY docker_database.ini database.ini

EXPOSE 5000

CMD ["python", "dechetAPI.py"]