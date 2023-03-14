FROM python:3.10

RUN mkdir /mytbot

WORKDIR /mytbot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

CMD docker compose build

CMD docker compose up