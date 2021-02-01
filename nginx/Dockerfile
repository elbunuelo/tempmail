# production environment
FROM nginx:stable-alpine
RUN apk update && apk upgrade && apk add bash

RUN rm -rf /usr/share/nginx/html/*
COPY nginx.conf /etc/nginx/conf.d/default.template
EXPOSE 80
