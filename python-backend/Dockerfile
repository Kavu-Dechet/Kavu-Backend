FROM python:3-slim

COPY requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt

RUN mkdir /tmp/images

COPY . /api
WORKDIR /api
COPY persistence/docker_database.ini persistence/database.ini

EXPOSE 5000

CMD ["python", "dechetAPI.py"]
