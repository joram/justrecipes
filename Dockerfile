FROM alpine:latest

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
ENV PYTHONUNBUFFERED=1

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 python3-dev && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN apk add --no-cache --virtual .build-deps gcc musl-dev mariadb-dev build-base libxslt-dev libxml2-dev python3-dev

# Scipy and numpy
#RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
#RUN apk add gcc gfortran python3 python3-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev libffi-dev
#RUN ln -s /usr/include/locale.h /usr/include/xlocale.h


WORKDIR /recipes
ADD requirements.txt .


RUN pip install -r requirements.txt
ADD api /recipes/api
ADD db /recipes/db
ADD utils.py /recipes/utils.py

EXPOSE 5000
ENV PYTHONPATH=/recipes
CMD python ./api/api.py
