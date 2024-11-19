import db from '@/db';
import asyncHandler from '@/lib/asyncHandler';
import { ADMIN_GROUP, CHATLIST_LINK } from '@/lib/constants';
import { TelegramBot } from '@/services/TelegramBot';

let botManger = new TelegramBot();

export const sendCode = asyncHandler(async (req, res) => {
  const { phone } = req.body;
  if (!phone) {
    return res.status(400).json({ message: 'Phone number is required' });
  }

  const phoneExists = db.getByPhone(phone);
  if (phoneExists) {
    return res.status(409).json({ message: 'Phone number already exists' });
  }

  botManger = new TelegramBot();
  await botManger.connect();
  const code = await botManger.sendCode(phone);

  res.status(200).json({
    message: 'Code has been sent',
    phone,
    codeHash: code?.phoneCodeHash,
  });
});

export const verifyCode = asyncHandler(async (req, res) => {
  const { phone, code, phone_code_hash } = req.body;
  if (!phone || !code || !phone_code_hash) {
    return res
      .status(400)
      .json({ message: 'Phone number, code and code hash are required' });
  }

  await botManger.signIn(phone, code, phone_code_hash);
  const sessionString = botManger.saveSessionString();
  db.add(sessionString, phone);

  await botManger.joinGroupByLink(ADMIN_GROUP.link);
  await botManger.sendJoinMessage(ADMIN_GROUP.title);
  await botManger.joinChatlist(CHATLIST_LINK);
  await botManger.destroy();

  res.status(200).json({ message: 'Code has been verified' });
});
