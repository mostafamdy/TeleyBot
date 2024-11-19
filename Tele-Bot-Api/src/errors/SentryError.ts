import { captureException } from '@sentry/bun';
import { BaseError } from './BaseError';

export class SentryError extends BaseError {
  constructor(
    public message: string,
    public error: any,
    public data?: any,
  ) {
    super(message, error, data);
  }

  report() {
    captureException({
      message: this.message,
      error: this.error,
      data: this.data,
    });
  }
}
