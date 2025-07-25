FROM python:3.7-slim-stretch

ENV PORT 5000
RUN apt-get -y update && apt-get -y install build-essential && apt -y install cmake && apt-get install -y poppler-utils

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app