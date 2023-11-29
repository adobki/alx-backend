// Redis Pub/Sub: Publishing and subcribing to messages through channels

import { createClient } from 'redis';

const client = await createClient()
  .on('error', err => console.error('Redis client not connected to the server:', err))
  .on('connect', () => console.log('Redis client connected to the server'));

/**
 * Publishes a message to a channel.
 * @param {string} message Message to be published to channel.
 * @param {number} time Delay (in ms) before publishing the message.
 */
function publishMessage(message, time) {
  if (typeof message !== 'string' || typeof time !== 'number') return;

  setTimeout(async () => {
    console.log('About to send', message);
    await client.PUBLISH('holberton school channel', message);
  }, time);
}

publishMessage('Holberton Student #1 starts course', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400);

// Kills the server after set timeout
// setTimeout(() => client.end(false), 1000);
