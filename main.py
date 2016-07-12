

import os
import json
import asyncio
import aiohttp
import logging

from nats.aio.client import Client
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# App Settings
ZKILLBOARD_REDISQ = 'http://redisq.zkillboard.com/listen.php'
NATS_SERVERS = os.environ.get('NATS_SERVERS', 'nats://127.0.0.1:4222')


async def run(loop):
  client = Client()
  servers = NATS_SERVERS.split(',')

  await client.connect(io_loop=loop, servers=servers)

  while True:
    with aiohttp.ClientSession() as session:
    async with session.get(ZKILLBOARD_REDISQ) as resp:
        print(resp.status)
        print(await resp.text())


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(loop))
  loop.close()
