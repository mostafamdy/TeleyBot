import { ApiError } from '@/errors';
import { extractHashFromLink } from '@/lib/utils';
import { useTryAsync } from 'no-try';
import { Api, type TelegramClient } from 'telegram';

export class ChatlistManager {
  constructor(private client: TelegramClient) {}

  async checkChatlistInvite(link: string) {
    const slug = extractHashFromLink(link);

    const [err, data] = await useTryAsync(() =>
      this.client.invoke(new Api.chatlists.CheckChatlistInvite({ slug })),
    );

    if (err) {
      throw new ApiError('Chatlist not found.', err.message, link);
    }

    return data;
  }

  async joinChatlist(link: string) {
    const slug = extractHashFromLink(link);
    const chats = await this.getChatlist(link);
    const peers = chats.map(chat => chat.id);

    const [err] = await useTryAsync(() =>
      this.client.invoke(new Api.chatlists.JoinChatlistInvite({ slug, peers })),
    );

    if (err) {
      throw new ApiError('Failed to join the chatlist.', err.message, link);
    }

    console.log('Successfully joined the chatlist');
  }

  async getChatlist(link: string) {
    const slug = extractHashFromLink(link);

    const [err, chatlist] = await useTryAsync(() =>
      this.client.invoke(new Api.chatlists.CheckChatlistInvite({ slug })),
    );

    if (err) {
      throw new ApiError('Failed to get chatlist.', err.message);
    }

    if (!chatlist) {
      throw new ApiError('Chatlist not found.', 'Chatlist not found.', link);
    }

    return chatlist.chats;
  }
}
