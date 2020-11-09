FROM python:3.9

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r ./requirements.txt
COPY . /app/

RUN useradd -ms /bin/bash  snowdog

USER snowdog