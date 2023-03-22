FROM python:3.10

RUN mkdir /mytbot

WORKDIR /mytbot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

RUN alembic upgrade head

CMD python main.py

