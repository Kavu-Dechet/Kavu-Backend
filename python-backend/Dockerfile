FROM python:3-slim

COPY requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt

RUN mkdir /tmp/images

COPY . /api
WORKDIR /api
COPY persistence/docker_database.ini persistence/database.ini
COPY wait-for-it.sh .

RUN chmod +x wait-for-it.sh

EXPOSE 5000

CMD ["./wait-for-it.sh", "kavu-database:5432", "--", "python", "dechetAPI.py"]
