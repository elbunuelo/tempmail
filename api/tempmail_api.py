from flask import Flask, request
from flask_cors import CORS
from email.parser import Parser
from uuid import uuid4

import redis
import os
import json
import random
import logging

from words import nouns, adjectives

DOMAIN = os.getenv('DOMAIN')

app = Flask(__name__)
CORS(app)

redis_client = redis.Redis(host='redis')

if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def get_mailbox():
    adjective_part = '.'.join(random.choices(adjectives, k=2))
    noun = random.choice(nouns)
    return f'{adjective_part}.{noun}'


@app.route('/mailbox', methods=['POST'])
def create_mailbox():
    token = str(uuid4())

    mailbox = get_mailbox()

    email_address = f'{mailbox}@{DOMAIN}'
    redis_client.set(token, json.dumps({ 'mailbox': email_address, 'emails': []}))
    redis_client.set(mailbox, token)

    return ({
        'mailbox': email_address,
        'token':  token
    }, 201)


@app.route('/email', methods=['POST'])
def create_email():
    email_data = request.json
    secret = request.headers.get('Authorization').split(' ')[-1]

    if secret != os.getenv('SECRET'):
       return '', 403

    for recipient in email_data['recipients']:
        mailbox = recipient.split('@')[0].split('+')[0]

        if redis_client.exists(mailbox):
            token = redis_client.get(mailbox)
            record  = json.loads(redis_client.get(token))
            emails = record.get('emails')
            emails.append(email_data)
            redis_client.set(token, json.dumps(record))

    return '', 201


@ app.route('/<token>', methods=['GET'])
def list_emails(token):

    if not redis_client.exists(token):
        return 'Mailbox does not exist', 404

    mailbox_data = json.loads(redis_client.get(token))
    return mailbox_data
