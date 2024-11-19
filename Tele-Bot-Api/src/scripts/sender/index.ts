import db from '@/db';
import { delay } from '@/lib/utils';
import { Worker } from 'node:worker_threads';

console.log('Starting the sender worker...');

// Refresh data by retrieving all bots with a valid messageId
const refreshData = () => db.getAll().filter(bot => bot.messageId);

// Function to start the worker threads
const startWorkers = () => {
  const onlineBots = refreshData();

  const chunkSize = 4;
  const botChunks = [];

  for (let i = 0; i < onlineBots.length; i += chunkSize) {
    botChunks.push(
      onlineBots.slice(i, i + chunkSize).map(bot => ({
        id: bot.id,
        phone: bot.phone,
        messageId: bot.messageId,
        session: bot.session,
      })),
    );
  }

  const getWorkerPath = (file: string) => new URL(`./${file}`, import.meta.url);

  let completedWorkers = 0;
  botChunks.forEach((botChunk, index) => {
    const worker = new Worker(getWorkerPath('./worker.ts'), {
      workerData: {
        bots: botChunk,
        workerId: index + 1,
      },
    });

    worker.on('message', message => {
      if (message.action === 'done') {
        console.log(`Worker ${index + 1} completed its tasks.`);
        completedWorkers++;
        if (completedWorkers === botChunks.length) {
          console.log('All workers completed their tasks.');
        }
      }
    });

    worker.on('error', error => {
      console.error(`Worker ${index + 1} encountered an error:`, error.message);
    });

    worker.on('exit', code => {
      if (code !== 0) {
        console.error(`Worker ${index + 1} stopped with exit code ${code}`);
      }
    });
  });
};

// Run the code forever
while (true) {
  startWorkers();
  // Add a delay between each iteration to avoid excessive resource usage
  await delay(1000 * 300); // 5 minutes
}
