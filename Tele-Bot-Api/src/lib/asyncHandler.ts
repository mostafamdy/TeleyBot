import { ApiError } from '@/errors';
import type { RequestHandler } from 'express';

export default function asyncHandler(callback: RequestHandler): RequestHandler {
  return async (req, res, next) =>
    await Promise.resolve(callback(req, res, next)).catch(err => {
      if (err instanceof ApiError) {
        res.status(500).json(err);
      } else if (err instanceof Error) {
        res.status(500).json({ message: err.message });
      } else {
        res.status(500).json({ message: 'An unknown error occurred' });
      }
    });
}
