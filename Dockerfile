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
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
#RUN apk add mariadb-connector-c-dev
#RUN apk add make perl
#RUN wget https://github.com/xianyi/OpenBLAS/archive/v0.3.6.tar.gz \
#	&& tar -xf v0.3.6.tar.gz \
#	&& cd OpenBLAS-0.3.6/ \
#	&& make BINARY=64 FC=$(which gfortran) USE_THREAD=1 \
#	&& make PREFIX=/usr/lib/openblas install
#RUN apk add libxslt-dev libxml2-dev python3-dev

WORKDIR /recipes
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD api /recipes/api
ADD recipes.json /recipes
ADD tags.json /recipes

EXPOSE 5000
CMD python /recipes/api/api.py
