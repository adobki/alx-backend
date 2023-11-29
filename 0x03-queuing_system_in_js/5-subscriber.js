// Redis Pub/Sub: Publishing and subcribing to messages through channels

import { createClient } from 'redis';

/**
 * Processes a message received from a subscribed channel.
 * @param {string} message Message received from a channel.
 */
function processMessage(message) {
  if (typeof message !== 'string') return;
  
  console.log(message);

  if (message === 'KILL_SERVER') {
    client.UNSUBSCRIBE();
    client.end(false);
    return;
  }
}

const client = await createClient()
  .on('error', err => console.error('Redis client not connected to the server:', err))
  .on('connect', () => console.log('Redis client connected to the server'));

client.SUBSCRIBE('holberton school channel');
client.on('message', (channel, message) => processMessage(message));
