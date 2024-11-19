import db from '@/db';
import asyncHandler from '@/lib/asyncHandler';

export const saveMessage = asyncHandler((req, res) => {
  const { start, end, messageId } = req.body;
  if (!start || !end || !messageId) {
    return res
      .status(400)
      .json({ message: 'Start, end, and message ID are required' });
  }

  const selectedBots = db.getAll().slice(start - 1, end);
  selectedBots.forEach(bot => db.updateMessageId(bot.id, messageId));
  res.status(200).json({ message: 'Message saved' });
});
