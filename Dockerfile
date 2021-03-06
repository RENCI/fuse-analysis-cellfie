FROM python:3.8-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk --no-cache add gcc musl-dev libffi-dev file make
RUN pip3 install --no-cache-dir flask greenlet==0.4.16 gevent==1.4.0 gunicorn==19.9.0 connexion[swagger-ui] oslash

COPY api /usr/src/app/api
COPY tx-utils/src /usr/src/app
COPY data /usr/src/app/data

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]

