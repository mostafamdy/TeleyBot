import cors from 'cors';
import express from 'express';
import responseTime from 'response-time';

import { SentryError } from './errors';
import { PORT } from './lib/constants';
import morganLogger from './lib/morgan';
import apiRouter from './routes';

import './lib/sentry';

const app = express();

app
  .use(express.json())
  .use(cors())
  .use(
    responseTime((_req, res, time) =>
      res.setHeader('response-time', time.toFixed(2)),
    ),
  )
  .use(morganLogger);

app.get('/', (_, res) => {
  res.json({ message: 'Hello World!' });
});

app.use('/api', apiRouter);

app.get('/debug-sentry', () => {
  throw new SentryError('Sentry Test Error', new Error('Sentry Test Error'));
});
app.all('*', (_, res) => res.status(404).json({ error: 'Not Found' }));

app.listen(PORT, () => console.log('Server is listening on port 3000'));
