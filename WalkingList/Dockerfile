FROM mdillon/postgis:10-alpine

RUN apk update
RUN apk add python3

RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories
RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
RUN apk update
RUN apk upgrade --update-cache --available

RUN apk add texlive

RUN apk add py3-psycopg2

