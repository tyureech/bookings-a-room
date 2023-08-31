FROM python:3.11

RUN mkdir bookeing-a-room

WORKDIR /booking-a-room

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
