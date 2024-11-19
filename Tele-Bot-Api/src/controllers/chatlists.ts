import db from '@/db';
import asyncHandler from '@/lib/asyncHandler';
import { CHATLIST_LINK } from '@/lib/constants';
import { TelegramBot } from '@/services/TelegramBot';

export const joinChatlist = asyncHandler(async (req, res) => {
  const bots = db.getAll();
  console.log(bots.length);

  for (const bot of bots) {
    const botManger = new TelegramBot(bot.session);
    await botManger.connect();
    await botManger.joinChatlist(CHATLIST_LINK);
  }

  res.status(req.statusCode || 200).json({ message: 'Joined chatlist' });
});
