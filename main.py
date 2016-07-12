

import json
import logging
import requests

from gcloud import pubsub

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# App Settings
ZKILLBOARD_REDISQ = 'http://redisq.zkillboard.com/listen.php'

# PubSub Settings
PS_CLIENT = pubsub.Client()
PS_TOPIC = PS_CLIENT.topic('zkillboard.raw')

if not PS_TOPIC.exists():
    PS_TOPIC.create()

while True:
    response = requests.get(ZKILLBOARD_REDISQ)
    
    if response.status_code == requests.codes.ok:
        data = response.json()
        
        if data['package'] is not None:
            killmail = data['package']
            logger.info('Got new killmail with ID {}'.format(killmail['killID']))

            PS_TOPIC.publish(json.dumps(killmail))
        
        else:
            logger.info('No new killmail.')
    
    else:
        logger.error('Problem with zKB response. Got code {}.'.format(response.status_code))
