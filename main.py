

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
        killmail = response.json()
        
        if killmail['package'] is not None:
            logger.info('Got new killmail with ID {}'.format(killmail['package']['killID']))

            PS_TOPIC.publish(json.dumps(killmail['package']))
        
        else:
            logger.info('No new killmail.')
    
    else:
        logger.error('Problem with zKB response. Got code {}.'.format(response.status_code))
