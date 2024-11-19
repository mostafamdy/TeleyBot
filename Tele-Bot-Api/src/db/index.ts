import { ApiError } from '@/errors';
import { Database } from 'bun:sqlite';
import { useTry } from 'no-try';
import { queries } from './queries';
import type { BannedBot, Bot } from './types';

class DbHandler {
  private db = new Database('bots.db');

  constructor() {
    this.db.exec(queries.createBotsTable);
    this.db.exec(queries.createBannedTable);
  }
  getAll(): Bot[] {
    const [err, data] = useTry(() => this.db.prepare(queries.getAllBots).all());

    if (err) {
      throw new ApiError('Failed to get all bots', err);
    }

    return data as Bot[];
  }

  getAllBanned(): BannedBot[] {
    const [err, data] = useTry(() =>
      this.db.prepare(queries.getAllBanned).all(),
    );

    if (err) {
      throw new ApiError('Failed to get all banned bots', err);
    }

    return data as BannedBot[];
  }

  add(session: Bot['session'], phone: Bot['phone']): void {
    useTry(
      () => this.db.prepare(queries.addBot).run(session, phone),
      err => {
        throw new ApiError('Failed to add bot', err);
      },
    );
  }

  delete(id: Bot['id']): void {
    useTry(
      () => this.db.prepare(queries.deleteBot).run(id),
      err => {
        throw new ApiError('Failed to delete bot', err);
      },
    );
  }

  get(id: Bot['id']): Bot | null {
    const [err, data] = useTry(() =>
      this.db.prepare(queries.getBotById).get(id),
    );

    if (err) {
      throw new ApiError('Failed to get bot by ID', err);
    }

    return data as Bot;
  }

  getByPhone(phone: Bot['phone']): Bot | BannedBot | null {
    const [err, bot] = useTry(() =>
      this.db.prepare(queries.getBotByPhone).get(phone),
    );

    if (err) {
      throw new ApiError('Failed to get bot by phone', err);
    }

    if (bot) {
      return bot as Bot;
    }

    const [bannedErr, bannedBot] = useTry(() =>
      this.db.prepare(queries.getBannedBotByPhone).get(phone),
    );

    if (bannedErr) {
      throw new ApiError('Failed to get banned bot by phone', bannedErr);
    }

    return bannedBot as BannedBot;
  }

  updateMessageId(id: Bot['id'], messageId: Bot['messageId']): void {
    useTry(
      () => this.db.prepare(queries.updateMessageId).run(messageId, id),
      err => {
        throw new ApiError('Failed to update message ID', err);
      },
    );
  }

  ban(
    id: Bot['id'],
    phone: Bot['phone'],
    joinedDate: BannedBot['joinedDate'],
  ): void {
    useTry(
      () => {
        this.db.prepare(queries.deleteBot).run(id);
        this.db.prepare(queries.banBot).run(phone, joinedDate);
      },
      err => {
        throw new ApiError('Failed to ban bot', err);
      },
    );
  }
}

export default new DbHandler();
