// Creates a job creator with Kue

import { createQueue } from 'kue';

const queue = createQueue();

const job = queue.create('push_notification_code', {
  phoneNumber: '555-WE-TIP', message: 'This is the code to verify your account',
})
  .save((err) => { if (!err) console.log('Notification job created:', job.id); })
  .on('complete', () => console.log('Notification job completed'))
  .on('failed', () => console.log('Notification job failed'));
