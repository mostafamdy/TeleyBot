import chalk from 'chalk';
import { BaseError } from './BaseError';
import { SentryError } from './SentryError';

export class ApiError extends BaseError {
  private sentryError: SentryError;

  constructor(
    public message: string,
    public error: any,
    public data?: any,
  ) {
    super(message, error, data);
    this.sentryError = new SentryError(message, error, data);
    this.log();
  }

  log() {
    console.log(chalk.bgRed(' Error '), this.toString());
  }
}
