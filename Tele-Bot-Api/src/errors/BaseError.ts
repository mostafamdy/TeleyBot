import chalk from 'chalk';

export class BaseError extends Error {
  constructor(
    public message: string,
    public error: any,
    public data?: any,
  ) {
    super(message);
    this.name = 'BaseError';
    Error.call(this, message);
    Error.captureStackTrace(this, this.constructor);
    Object.defineProperty(this, 'name', {
      value: this.constructor.name,
      configurable: true,
    });
  }

  private getError() {
    return {
      name: this.name,
      message: this.message,
      error: this.error,
      data: this.data,
    };
  }

  toJSON() {
    return JSON.parse(JSON.stringify(this.getError(), null, 2));
  }

  toString() {
    return JSON.stringify(this.getError(), null, 2)
      .replace(/: (\d+)/g, (_, p1) => `: ${chalk.yellow(p1)}`) // numbers
      .replace(/: "([^"]+)"/g, (_, p1) => `: ${chalk.green(`"${p1}"`)}`) // string
      .replace(/"([^"]+)":/g, (_, p1) => chalk.blue(`"${p1}":`)); // keys
  }

  static fromError(error: any, data?: any) {
    return new BaseError(error.message, error, data);
  }

  static fromMessage(message: string, data?: any) {
    return new BaseError(message, null, data);
  }
}
