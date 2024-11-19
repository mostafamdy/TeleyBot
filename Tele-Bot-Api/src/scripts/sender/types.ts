import type { TelegramBot } from '@/services/TelegramBot';

export type SenderBot = {
  id: number;
  phone: string;
  messageId: number;
  session: string;
  bot: TelegramBot;
  joinedDate: string;
};
