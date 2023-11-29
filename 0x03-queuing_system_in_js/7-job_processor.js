// Job processor for creating jobs and processing them while tracking their
// progress and errors with Kue and Redis

import { createQueue } from 'kue';

/**
 * Kue Job processor that mocks sending a notification message to a phone number.
 * @param {string} phoneNumber Recipient of the message.
 * @param {string} message Message to be sent.
 * @param {object.<kue.Job>} job Kue Job object for the current job.
 * @param {function} done Callback function to signal job completion.
 */
function sendNotification(phoneNumber, message, job, done) {
  const blacklist = ['4153518780', '4153518781'];

  job.progress(0, 100);
  if (blacklist.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
  job.progress(50, 100);
  return done();
}

const queue = createQueue();
queue.process('push_notification_code_2', 2, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
