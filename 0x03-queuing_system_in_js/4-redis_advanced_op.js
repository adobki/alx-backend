// Node Redis client and advanced operations

import { createClient, print } from 'redis';

const client = await createClient()
  .on('error', err => console.error('Redis client not connected to the server:', err))
  .on('connect', () => console.log('Redis client connected to the server'));

function createHash(key, field, value) {
  client.HSET(key, field, value, print);
}

function getHash(key) {
  client.HGETALL(key, (err, val) => console.log(val));
}

function deleteHash(key, values) {
  for (const item of values) {
    client.HDEL(key, item[0]);
  }
}

const key = 'HolbertonSchools';
const values = [
  ['Portland', 50],
  ['Seattle', 80],
  ['New York', 20],
  ['Bogota', 20],
  ['Cali', 40],
  ['Paris', 2],
];
for (const value of values) {
  createHash(key, ...value);
}
getHash(key);

// Delete fields in hash
// deleteHash(key, values);
// getHash(key);
