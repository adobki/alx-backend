// Creates a job processor with Kue

import { createQueue, Job } from 'kue';

/**
 * Mocks sending a notification message to a phone number.
 * @param {string} phoneNumber Recipient of the message.
 * @param {string} message Message to be sent.
 */
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

const queue = createQueue();
queue.process('push_notification_code', (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message);
});
