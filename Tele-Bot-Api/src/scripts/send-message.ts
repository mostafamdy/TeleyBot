import db from '@/db';
import { ApiError, errors } from '@/errors';
import { CHATLIST_LINK } from '@/lib/constants';
import { eventManager } from '@/services/EventManager';
import { TelegramBot } from '@/services/TelegramBot';
import chalk from 'chalk';
import { useTryAsync } from 'no-try';

type Bot = {
  bot: TelegramBot;
  messageId: number;
  id: number;
  phone: string;
  session: string;
  joinedDate: string;
};

console.log('Bot script started!');
const bots: Bot[] = [];

// Refresh data by retrieving all bots with a valid messageId
const refreshData = () => db.getAll().filter(bot => bot.messageId);

// Restart sessions for all available bots
const restartSessions = async (diff: number) => {
  console.log('Restarting sessions...');
  if (diff < 0) {
    return bots;
  }

  const availableBots = refreshData().slice(-diff); // Get new bots
  const result = await Promise.allSettled(
    availableBots.map(async availableBot => {
      const bot = new TelegramBot(availableBot.session);
      await bot.connect();
      return { bot, ...availableBot };
    }),
  );

  // Handle errors and push connected bots to the array
  result.forEach((res, i) => {
    if (res.status === 'rejected') {
      new ApiError('Failed to restart session.', res.reason, {
        id: availableBots[i].id,
        phone: availableBots[i].phone,
      });
      db.ban(
        availableBots[i].id,
        availableBots[i].phone,
        availableBots[i].joinedDate,
      );
    } else {
      console.log(`Bot ${res.value.id} connected!`);
      bots.push(res.value);
    }
  });

  return bots;
};

// Initialize online bots
let onlineBots = await restartSessions(0);
const chatlistGroups = await bots.at(-1)!.bot.getChatlist(CHATLIST_LINK);
const reversedChatlist = chatlistGroups.toReversed();
const sendMessages = async () => {
  //@ts-ignore
  const promises = reversedChatlist.map(async ({ title }, i) => {
    console.log(`Sending message to group ${title}...`);
    const sendPromises = onlineBots.map(
      async ({ bot, phone, messageId, id, joinedDate }) => {
        const errorHandler = async (error: ApiError['message']) => {
          console.log(chalk.red(`Bot ${id} failed to send message!`));
          if (error?.includes(errors.deactivatedBan)) {
            console.log(chalk.red(`Bot ${id} is banned!`));
            db.ban(id, phone, joinedDate);
            onlineBots.splice(i, 1);
          } else if (
            error?.includes(errors.channelBan) ||
            error?.includes(errors.chatForbidden)
          ) {
            console.log(chalk.red(`Bot ${id} is banned in channel!`));
            bot.leaveGroup(title);
          }
          new ApiError('Failed to send message to group.', error, {
            id,
            phone,
          });
        };
        eventManager.once('error', errorHandler);

        const botGroups = await bot.getGroups();
        const botGroup = botGroups?.find(botGroup => botGroup.title === title);
        if (!botGroup) {
          console.log(`Bot ${id} is not in group ${title}!`);
          return;
        }

        console.log(`Bot ${id} sending message...`);
        await useTryAsync(() =>
          bot.forwardMessageToGroup(messageId, botGroup?.id!),
        );

        eventManager.removeListener('error', errorHandler);
      },
    );

    await Promise.allSettled(
      sendPromises.map(promise => setTimeout(() => promise, 30000)), // Delay between each message
    );
  });

  await Promise.allSettled(
    promises.map(promise => setTimeout(() => promise, 30000)),
  ); // Delay between each group
};

await sendMessages();

const newOnlineBots = refreshData();
if (newOnlineBots.length !== onlineBots.length) {
  onlineBots = await restartSessions(newOnlineBots.length - onlineBots.length);
}
