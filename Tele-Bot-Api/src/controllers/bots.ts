import db from '@/db';
import asyncHandler from '@/lib/asyncHandler';

export const getAllBots = asyncHandler(async (req, res) => {
  const bots = db.getAll();
  res.status(200).json({ data: bots });
});

export const getBotsCount = asyncHandler(async (req, res) => {
  const bots = db.getAll();
  const bannedBots = db.getAllBanned();

  const unavailableBots = bots.filter(bot => bot.messageId).length;
  const availableBots = bots.length - unavailableBots;

  res.status(200).json({
    data: {
      available: availableBots,
      unavailable: unavailableBots,
      banned: bannedBots.length,
    },
    message: 'Bots count',
  });
});
