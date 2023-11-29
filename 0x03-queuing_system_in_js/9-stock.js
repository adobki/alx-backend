// Implements an inventory management system with an Express API and a Redis database

import express from 'express';
import { createClient } from 'redis';

const app = express();
const port = 1245;
const client = createClient()
  .on('error', err => console.error('Redis client not connected to the server:', err))
  .on('connect', () => console.log('Redis client connected to the server'));
const listProducts = [
  {
    id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  }, {
    id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  }, {
    id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  }, {
    id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

/**
 * Adds/updates a product's attribute to the database.
 * @param {string|number} key ID of product to add/update.
 * @param {string} field Attribute to add/update.
 * @param {string} value Attribute's value.
 * @returns {boolean} `true` on success, `false` otherwise.
 */
function createHash(key, field, value) {
  return client.HSET(key, field, value);
}

/**
 * Asynchrously retrieves a product from the database by ID.
 * @param {string|number} key ID of product to retrieve.
 * @param {boolean} all ID of product to retrieve.
 * @returns {Promise<object|Error>}
 */
function getHash(key, all) {
  return new Promise((resolve) => {
    client.HGETALL(key, (err, obj) => {
      if (err) resolve();
      if (!obj || all) resolve(obj);
      // eslint-disable-next-line no-param-reassign
      else delete obj.currentQuantity; resolve(obj);
    });
  });
}

/**
 * Searches for product in DB by given ID and returns product if found.
 * @param {string|number} id ID of the requested product.
 * @returns {Promise<object|Error>} A product with the given id if it exists.
 */
function getItemById(id) {
  return getHash(id);
}

/**
 * Creates a reservation for a product in the database by its ID.
 * @param {string|number} itemId ID of product to reserve.
 * @param {number} stock number of units to reserve.
 */
function reserveStockById(itemId, stock) {
  return new Promise((resolve) => {
    getCurrentReservedStockById(itemId).then(obj => {
      if (!obj || obj.currentQuantity - stock < 0) resolve();
      resolve(createHash(obj.itemId, 'currentQuantity', Number(obj.currentQuantity) - stock));
    });
  });
}

/**
 * Asynchrously retrieves the reserved stock for a product in the database by its ID.
 * @param {string|number} itemId ID of product to retrieve.
 * @returns {promise<number|Error|null>} Reserved stock for the item.
 */
async function getCurrentReservedStockById(itemId) {
  return new Promise((resolve) => {
    getHash(itemId, 'all').then(obj => {
      if (!obj) resolve();
      resolve(obj);
    });
  });
}

/**
 * Logs a request summary to the console after a request is made to an Express API.
 * @param {Response} response - A response object from an API call.
 */
function logRequest(response) {
  if (response.req.params.length) {
    console.log(response.req.method, `"${response.req.url}"`, response.req.params, response.statusCode);
  } else {
    console.log(response.req.method, `"${response.req.url}"`, response.statusCode);
  }
}

app.get('/favicon.ico', (request, response) => {
  response.sendFile(`${process.cwd()}/favicon.ico`);
  if (response.statusCode === 304) response.statusCode = 200; // Ignore redirect on trailing slash
  logRequest(response);
});

app.get('/list_products', (request, response) => {
  Promise.all(listProducts.map((product) => getItemById(product.id))).then((products) => {
    response.send(products);

    if (response.statusCode === 304) response.statusCode = 200; // Ignore redirect on trailing slash
    logRequest(response);
  });
});

app.get('/list_products/:itemId', (request, response) => {
  getCurrentReservedStockById(request.params.itemId).then(obj => {
    if (obj) response.send(obj);
    else response.status(404).send({ status: 'Product not found' });

    if (response.statusCode === 304) response.statusCode = 200; // Ignore redirect on trailing slash
    logRequest(response);
  });
});

app.get('/reserve_product/:itemId', (request, response) => {
  getCurrentReservedStockById(request.params.itemId).then(obj => {
    if (!obj) response.status(404).send({ status: 'Product not found' });
    else if (obj.currentQuantity <= 0) {
      response.status(404).send({ status: 'Not enough stock available', itemId: obj.id });
    } else {
      reserveStockById(obj.itemId, 1);
      response.send({ status: 'Reservation confirmed', itemId: obj.itemId });
    }

    if (response.statusCode === 304) response.statusCode = 200; // Ignore redirect on trailing slash
    logRequest(response);
  });
});

app.all('*', (request, response) => {
  response.status(404).send('Error: 404 Not found!');
  logRequest(response);
});

app.listen(port, () => {
  console.log(`API available on localhost:${port}`);
});

/**
 * Serialises objects in an array and stores them in a Redis database as HASHes.
 * @param {Array.<object>} objects - An array of objects to be serialised.
 */
function addObjectsToDb(objects) {
  if (!objects || !Array.isArray(objects)) return;

  objects.map(obj => {
    createHash(obj.id, 'itemId', obj.id);
    createHash(obj.id, 'itemName', obj.name);
    createHash(obj.id, 'price', obj.price);
    createHash(obj.id, 'currentQuantity', obj.stock);
    createHash(obj.id, 'initialAvailableQuantity', obj.stock);
  });
}

// Populate database with products in `listProducts` array
client.on('connect', () => {
  addObjectsToDb(listProducts);
});
