import chalk from 'chalk';
import { parentPort, workerData } from 'node:worker_threads';

import { ApiError, errors } from '@/errors';
import { eventManager } from '@/services/EventManager';
import { TelegramBot } from '@/services/TelegramBot';

import db from '@/db';
import { ADMIN_GROUP } from '@/lib/constants';
import { useTryAsync } from 'no-try';
import type { SenderBot } from './types';

const bots: SenderBot[] = [];
for (const { id, phone, messageId, session, joinedDate } of workerData.bots) {
  const bot = new TelegramBot(session);
  await bot.connect();
  bots.unshift({ id, phone, messageId, session, bot, joinedDate });
}

const handleErrors = (
  error: ApiError['message'],
  { id, joinedDate, phone }: { id: number; phone: string; joinedDate: string },
  group: string,
  bot: TelegramBot,
) => {
  console.log(chalk.red(`Bot ${id} failed to send message!`));
  if (error?.includes(errors.deactivatedBan)) {
    console.log(chalk.red(`Bot ${id} is banned!`));
    db.ban(id, phone, joinedDate);
  } else if (
    error?.includes(errors.channelBan) ||
    error?.includes(errors.chatForbidden)
  ) {
    console.log(chalk.red(`Bot ${id} is banned in channel!`));
    bot.leaveGroup(group);
    parentPort?.postMessage({ action: 'leave', id, phone });
  } else {
    new ApiError('Failed to send message to group.', error, {
      id,
      phone,
    });
  }
};

for (const { bot, phone, messageId, id, joinedDate } of bots) {
  const botGroups = await bot.getGroups();
  if (!botGroups) {
    console.log(chalk.red(`Bot ${id} has no groups!`));
    continue;
  }
  for (const { id: groupId, title } of botGroups) {
    if (title === ADMIN_GROUP.title || !title) continue;
    console.log(`Bot ${id} sending message to group ${title}`);
    await useTryAsync(() => bot.forwardMessageToGroup(messageId, groupId!));
    eventManager.once('error', (error: ApiError['message']) =>
      handleErrors(error, { id, phone, joinedDate }, title, bot),
    );
  }
}

parentPort?.postMessage({ action: 'done' });
