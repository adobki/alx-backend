// Node Redis client and basic operations

import { createClient, print } from 'redis';

const client = await createClient()
  .on('error', err => console.error('Redis client not connected to the server:', err))
  .on('connect', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, val) => console.log(val));
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
