// Job creator for creating jobs and processing them while tracking their
// progress and errors with Kue and Redis

import { createQueue } from 'kue';

const queue = createQueue();
const jobs = [
  { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
  { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153518743', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4153538781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153118782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4153718781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4159518782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4158718781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4153818782', message: 'This is the code 4321 to verify your account' },
  { phoneNumber: '4154318781', message: 'This is the code 4562 to verify your account' },
  { phoneNumber: '4151218782', message: 'This is the code 4321 to verify your account' },
];

/**
 * Job creator. Creates and enqueus jobs with Kue.
 * @param {Array.<object>} jobs Array of objects to be queued as jobs.
 * @param {object.<kue.Queue>} queue kue Queue to create jobs in.
 */
export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) throw new Error('jobs is not an array');
  for (const task of jobs) {
    const job = queue.create('push_notification_code_3', task)
      .save((err) => { if (!err) console.log(`Notification job created: ${job.id}`); })
      .on('complete', () => console.log(`Notification job ${job.id} completed`))
      .on('progress', (progress) => console.log(`Notification job ${job.id} ${progress}% complete`))
      .on('failed', (err) => console.log(`Notification job ${job.id} failed: ${err}`));
  }
}

// createPushNotificationsJobs(jobs, queue);
