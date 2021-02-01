#! /usr/bin/python3

import os
import sys
import json
import requests
import base64
from email.parser import Parser
from email import policy

email = Parser(policy=policy.SMTP).parse(sys.stdin)


secret = os.getenv('SECRET')
headers = {
    'User-Agent': 'tempmail/service',
    'Authorization': f'Bearer {secret}'
}

data = {
    'sender':sys.argv[1],
    'recipients' : sys.argv[2:],
    'headers': { k:v  for k,v in email.items()},
    'body': email.get_body().as_string(),
}

requests.post(f'http://server/api/email', json=data, headers=headers)
