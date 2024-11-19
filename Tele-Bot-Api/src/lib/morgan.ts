import chalk from 'chalk';
import type { Request, Response } from 'express';
import morgan from 'morgan';

// Apply color to the status code
morgan.token('status', (req: Request, res: Response) => {
  const status = res.statusCode;
  const color =
    status >= 500
      ? 'red'
      : status >= 400
        ? 'yellow'
        : status >= 300
          ? 'cyan'
          : status >= 200
            ? 'green'
            : 'white';
  return chalk[color](status);
});

// Apply color to the method
morgan.token('method', (req: Request, res: Response) => {
  const method = req.method;
  const color =
    method === 'GET'
      ? 'green'
      : method === 'POST'
        ? 'yellow'
        : method === 'PUT'
          ? 'cyan'
          : method === 'DELETE'
            ? 'red'
            : 'white';
  return chalk[color](method);
});

// Apply color to the URL
morgan.token('url', (req: Request, res: Response) => {
  const url = req.url;
  const color = url.includes('error') ? 'red' : 'white';
  return chalk[color](url);
});

// Apply color to the response time
morgan.token('response-time', (req: Request, res: Response) => {
  const time = Number(res.get('response-time')) as number;
  const color =
    time < 100
      ? 'green'
      : time < 500
        ? 'yellow'
        : time < 1000
          ? 'red'
          : 'white';
  return chalk[color](time);
});

// Apply color to the date
morgan.token('date', () => {
  return chalk.white(
    new Date().toLocaleDateString('en-US', {
      hourCycle: 'h23',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZoneName: 'short',
    }),
  );
});

// Create a custom morgan format
const format = ':date :method :url :status :response-time ms';

// Create a morgan middleware
const morganLogger = morgan(format);

export default morganLogger;
