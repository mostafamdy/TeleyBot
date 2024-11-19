import { ApiError } from '@/errors';
import type { ErrorRequestHandler } from 'express';

export const globalErrorHandler: ErrorRequestHandler = (
  err,
  _req,
  res,
  _next,
) => {
  new ApiError('Internal Server Error', err);
  res.status(500).json({ error: 'Internal Server Error' });
};
