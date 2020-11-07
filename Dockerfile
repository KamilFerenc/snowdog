FROM python:3.9

WORKDIR /app
COPY ./doc/requirements/base.txt /app/doc/requirements/
RUN pip install -r ./doc/requirements/base.txt
COPY . /app/

RUN useradd -ms /bin/bash  snowdog

USER snowdog