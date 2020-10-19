FROM ubuntu:18.04

RUN apt-get -qq update \
 && apt-get -qq install locales python3-pip gunicorn3 \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s /usr/bin/python3 /usr/bin/python \
 && ln -s /usr/bin/gunicorn3 /usr/bin/gunicorn \
 && locale-gen en_US.UTF-8

ENV LC_ALL en_US.UTF-8

RUN pip3 install --upgrade pip
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR app

COPY bert ./bert

COPY common.py ./
COPY config.py ./
COPY conlleval.py ./
COPY ner.py ./
COPY so2html.py ./
COPY serve.py ./

RUN chgrp -R 0 /app \
 && chmod -R g+rwX /app

EXPOSE 5000

USER 9008

COPY run /run.sh

ENV GUNICORN_WORKER_AMOUNT 1
ENV GUNICORN_TIMEOUT 300
ENV GUNICORN_RELOAD ""

ENV NER_MODEL_DIR /app/models/ner

ENTRYPOINT [ "/run.sh" ]