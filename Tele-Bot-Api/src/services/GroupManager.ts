import { ApiError } from '@/errors';
import { extractHashFromLink } from '@/lib/utils';
import { useTryAsync } from 'no-try';
import { Api, TelegramClient } from 'telegram';
import type { EntityLike } from 'telegram/define';

export class GroupManager {
  constructor(private client: TelegramClient) {}

  async getGroups() {
    const [err, chats] = await useTryAsync(() => this.client.getDialogs());
    if (err) {
      throw new ApiError('Failed to get dialogs.', err.message);
    }

    return chats?.filter(chat => chat.isGroup).reverse();
  }

  async sendJoinMessage(title: string) {
    const [meError, me] = await useTryAsync(() => this.client.getMe());
    if (meError) {
      throw new ApiError('Failed to get self info.', meError);
    }

    const dialogs = await this.client.getDialogs();
    const chat = dialogs?.find(chat => chat.title === title);
    if (!chat) {
      throw new ApiError('Group not found.', 'Group not found.', {
        title,
      });
    }

    const [err] = await useTryAsync(() =>
      this.client.sendMessage(chat.id!, {
        message: `Hello, I'm ${me?.firstName}`,
      }),
    );

    if (err) {
      throw new ApiError('Failed to send join message.', err.message, {
        title,
      });
    }

    console.log('Successfully sent the join message');
  }

  async sendGroupMessage(groupId: EntityLike, message: string) {
    const [err2] = await useTryAsync(() =>
      this.client.sendMessage(groupId, { message }),
    );

    if (err2) {
      throw new ApiError('Failed to send message.', err2.message, {
        groupId,
        message,
      });
    }

    console.log('Successfully sent the message');
  }

  async leaveGroup(groupTitle: string) {
    const [err, chats] = await useTryAsync(() => this.client.getDialogs());
    if (err) {
      new ApiError('Failed to get dialogs.', err.message);
      return;
    }

    const [getMeError, me] = await useTryAsync(() => this.client.getMe());
    if (getMeError) {
      throw new ApiError('Failed to get self info.', getMeError);
    }

    const group = chats?.find(chat => chat.title === groupTitle);

    if (!group) {
      throw new ApiError('Group not found.', 'Group not found.', {
        groupTitle,
      });
    }

    const [err2] = await useTryAsync(() =>
      this.client.invoke(new Api.channels.LeaveChannel({ channel: group.id })),
    );

    if (err2) {
      throw new ApiError('Failed to leave the group.', err2.message, {
        groupTitle,
      });
    }

    console.log('Successfully left the group');
  }

  async joinGroupByLink(link: string) {
    const hash = extractHashFromLink(link);
    const [err] = await useTryAsync(() =>
      this.client.invoke(new Api.messages.ImportChatInvite({ hash })),
    );

    if (err) {
      throw new ApiError('Failed to join the group.', err.message, {
        link,
      });
    }

    console.log('Successfully joined the group');
  }

  async joinGroupByTitle(groupTitle: string) {
    const [err, chats] = await useTryAsync(() => this.client.getDialogs());
    if (err) {
      new ApiError('Failed to get dialogs.', err.message);
      return;
    }

    const [getMeError, me] = await useTryAsync(() => this.client.getMe());
    if (getMeError) {
      throw new ApiError('Failed to get self info.', getMeError);
    }

    const group = chats?.find(chat => chat.title === groupTitle);

    if (!group) {
      throw new ApiError('Group not found.', 'Group not found.', {
        groupTitle,
      });
    }

    const [err2] = await useTryAsync(() =>
      this.client.invoke(new Api.channels.JoinChannel({ channel: group.id })),
    );

    if (err2) {
      throw new ApiError('Failed to join the group.', err2.message, {
        groupTitle,
      });
    }

    console.log('Successfully joined the group');
  }

  async getGroupMessages(groupTitle: string) {
    const [err1, chats] = await useTryAsync(() => this.client.getDialogs());
    if (err1) {
      new ApiError('Failed to get dialogs.', err1.message);
      return;
    }
    const group = chats?.find(chat => chat.title === groupTitle);

    if (!group) {
      throw new ApiError('Group not found.', 'Group not found.', {
        groupTitle,
      });
    }

    const [err2, groupMessages] = await useTryAsync(() =>
      this.client.getMessages(group.id, { reverse: true }),
    );
    if (err2) {
      throw new ApiError('Failed to get group messages.', err2.message, {
        groupTitle,
      });
    }

    return groupMessages?.filter(message => message.message);
  }
}
