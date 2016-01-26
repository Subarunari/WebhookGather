# WebhookGather
WebhookGather is Proxy for Incoming Webhook.

## Motivation
The purpose is to aggregate Incoming Webhook Configuration.

Many applications is connected to many applications By Web API.
Web API config is stored in each application. 
Being increased the number of application, maintenance costs for Web API config will be increased.
Maintenance is so bored...Concentrate to development!!

## Usage 
To run server, execute follow command.
`$ python app.py`

Typing Ctrl-C, Server is stopped.

## Architecture
* python 3.4.2 
* tornado 4.2
* Logbook 0.1

# ToDo
* Create web client for setting webhook.ini
    * Change DB from webhook.ini
* Add UnitTest
* Add Detail Description
* Create setup.py
