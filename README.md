# Tempmail - Self hosted disposable email

Some sites have started blocking sign-up using well known disposable email
services such as [meltmail](https://meltmail.com) or
[10minutemail](https://10minutemail.com). This project is a solution to that
problem, allowing you to host your own solution with whatever domain you
choose.

## Quick Start

The whole project runs on docker containers, so you should be able to run it
anywhere where `docker` and `docker-compose` is available.

### DNS Setup

You need to have a registered domain name and be able to edit its DNS settings.
Create `A` and `MX` records pointing to where the service is deployed and
enable ports 80 (HTTP) and 25 (SMTP).

### Configuration

The service configuration values can be found in the `.env` file. You need to
set two values: `DOMAIN` with your domain name and `SECRET` to a random 64
character string.

### Running

After all the necessary set up, clone the repository and run
`docker-compose up -d` on the project directory for building and starting the
different services.

After all the images have been downloaded and the containers set up, you
should be able to access the front end by accessing `http://yourdomain.com/`.
When you do so, you will be presented with a disposable email address you can
start using right away.

## SMTP Server

The email server used for this project is Postfix, it's configured to act as a
destination only server for the configured domain. All received emails are
piped to a python script which parses it and sends it to the API.

## API

The Flask API that serves as the back bone of the service is pretty simple,
consisting of just three endpoints for requesting a mailbox, creating emails
from the SMTP server and getting the emails received for a particular mailbox.

## Front End

The Front end is built in React and consists of a single screen that requests a
new Mailbox to the API on load and then polls the API every 10 seconds asking
for new messages.
