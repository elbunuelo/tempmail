FROM alpine:3.10

RUN adduser --disabled-password --system tempmail
RUN apk add --no-cache --update postfix cyrus-sasl cyrus-sasl-plain ca-certificates bash && \
    apk add --no-cache --upgrade musl musl-utils && \
    apk add --no-cache --upgrade python3 && \
    (rm "/tmp/"* 2>/dev/null || true) && (rm -rf /var/cache/apk/* 2>/dev/null || true)


RUN pip3 install requests

EXPOSE 25

RUN mkdir -p /opt/email/
COPY process_email.py /opt/email/
RUN chown -R tempmail: /opt/email/

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

