

import os
import json
import pika
import logging
import requests


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# App Settings
ZKILLBOARD_REDISQ = 'http://redisq.zkillboard.com/listen.php'
RABBITMQ_SERVER = os.environ.get('RABBITMQ_SERVER', 'rabbitmq-alpha')

# RabbitMQ Setup
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_SERVER))
channel = connection.channel()

channel.exchange_declare(exchange='regner', type='topic')
logger.info('Connected to RabbitMQ server...')

while True:
    response = requests.get(ZKILLBOARD_REDISQ)
    
    if response.status_code == requests.codes.ok:
        data = response.json()
        
        if data['package'] is not None:
            killmail = data['package']

            logger.info('Publishing new killmail with ID {}.'.format(killmail['killID']))

            channel.basic_publish(
                exchange='regner',
                routing_key='zkillboard.raw',
                body=json.dumps(killmail),
                properties=pika.BasicProperties(
                    delivery_mode = 2,
                ),
            )
        
        else:
            logger.info('No new killmail.')
    
    else:
        logger.error('Problem with zKB response. Got code {}.'.format(response.status_code))
