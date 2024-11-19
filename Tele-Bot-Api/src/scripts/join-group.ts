import db from '@/db';
import { TelegramBot } from '@/services/TelegramBot';

const groupLink = 'https://t.me/+ARDD4CT99pAyMWIy';
const bots = db.getAll();

for (const bot of bots) {
  const client = new TelegramBot(bot.session);
  await client.connect();
  client.joinGroupByLink(groupLink);
}
