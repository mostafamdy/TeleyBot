import { ApiError } from '@/errors';
import { useTryAsync } from 'no-try';
import { Api, TelegramClient } from 'telegram';
import type { EntityLike } from 'telegram/define';
import { eventManager } from './EventManager';

export class MessageManager {
  constructor(private client: TelegramClient) {}

  async forwardMessageToGroup(
    messageId: number,
    from: EntityLike,
    to: EntityLike,
  ) {
    const [err] = await useTryAsync(() =>
      this.client.invoke(
        new Api.messages.ForwardMessages({
          fromPeer: from,
          id: [messageId],
          toPeer: to,
          dropAuthor: false,
          dropMediaCaptions: false,
        }),
      ),
    );

    if (err) {
      eventManager.emit('error', err.message);
      throw new ApiError('forwardMessageToGroup Error.', err.message);
    }

    console.log('Messages sent to group!');
  }

  async forwardMessageToAllGroups(
    messageId: number,
    from: string,
    execludedGroups?: string[],
  ) {
    const [getDialogsError, chats] = await useTryAsync(() =>
      this.client.getDialogs(),
    );

    if (getDialogsError) {
      eventManager.emit('error', getDialogsError.message);
      throw new ApiError('Failed to get dialogs.', getDialogsError);
    }

    const groups = chats
      ?.filter(chat => chat.isGroup && !execludedGroups?.includes(chat.title!))
      .reverse();

    if (!groups) {
      throw new ApiError('No groups found.', null);
    }

    for (const group of groups) {
      const [err] = await useTryAsync(() =>
        this.forwardMessageToGroup(messageId, from, group.id!),
      );

      console.log(group.title);

      if (err) {
        throw new ApiError(
          'Failed to send message to all groups.',
          err.message,
        );
      }
    }

    console.log('Messages sent to all groups!');
  }
}
