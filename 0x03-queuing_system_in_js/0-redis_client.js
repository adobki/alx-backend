// Node Redis Client

import { createClient } from 'redis';

const client = createClient()
  .on('error', err => console.error('Redis client not connected to the server:', err))
  .on('connect', () => console.log('Redis client connected to the server'));
