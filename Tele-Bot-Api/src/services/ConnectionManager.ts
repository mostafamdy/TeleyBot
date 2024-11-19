import { ApiError } from '@/errors';
import { useTry, useTryAsync } from 'no-try';
import { Api, TelegramClient } from 'telegram';

export class ConnectionManager {
  constructor(private client: TelegramClient) {}

  async isConnectionReady() {
    const [err, data] =
      (await useTryAsync(() => this.client.isUserAuthorized())) ||
      this.client.connected;

    if (err) {
      throw new ApiError('Connection check failed.', err.message);
    }
    return data;
  }

  async connect() {
    const [err] = await useTryAsync(() => this.client.connect());

    if (err) {
      throw new ApiError('Connection failed.', err.message);
    }
  }

  async disconnect() {
    const [err] = await useTryAsync(() => this.client.disconnect());

    if (err) {
      throw new ApiError('Disconnection failed.', err.message);
    }
  }

  async destroy() {
    const [err] = await useTryAsync(() => this.client.destroy());

    if (err) {
      throw new ApiError('Disconnection failed.', err.message);
    }
  }

  async start(phoneNumber: string, phoneCode: string) {
    const [err] = await useTryAsync(() =>
      this.client.start({
        phoneNumber,
        phoneCode: async () => phoneCode,
        onError: console.error,
      }),
    );

    if (err) {
      throw new ApiError('Starting failed.', err.message, {
        phoneNumber,
      });
    }

    console.log('You are now connected.');
  }

  async signIn(phoneNumber: string, phoneCode: string, codeHash: string) {
    const [err] = await useTryAsync(() =>
      this.client.invoke(
        new Api.auth.SignIn({
          phoneNumber: phoneNumber,
          phoneCode: phoneCode,
          phoneCodeHash: codeHash,
        }),
      ),
    );

    if (err) {
      throw new ApiError('Starting failed.', err.message, {
        phoneNumber,
      });
    }

    console.log('You are now connected.');
  }

  async sendCode(phoneNumber: string) {
    const [err, data] = await useTryAsync(() =>
      this.client.sendCode(
        { apiHash: this.client.apiHash, apiId: this.client.apiId },
        phoneNumber,
      ),
    );

    if (err) {
      throw new ApiError('Sending code failed.', err.message, {
        phoneNumber,
      });
    }

    return data;
  }

  saveSessionString() {
    const [err, data] = useTry(() => this.client.session.save());
    if (err) {
      throw new ApiError('Saving session failed.', err.message);
    }
    return data as unknown as string;
  }
}
