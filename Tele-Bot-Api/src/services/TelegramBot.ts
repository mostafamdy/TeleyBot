import { TelegramClient, sessions } from 'telegram';
import type { EntityLike } from 'telegram/define';

import { ADMIN_GROUP, API } from '@/lib/constants';

import { ChatlistManager } from './ChatlistManager';
import { ConnectionManager } from './ConnectionManager';
import { GroupManager } from './GroupManager';
import { MessageManager } from './MessageManager';

export class TelegramBot {
  private connectionManager: ConnectionManager;
  private groupManager: GroupManager;
  private messageManager: MessageManager;
  private chatlistManager: ChatlistManager;

  constructor(
    stringSession: string = '',
    apiId: number = API.id,
    apiHash: string = API.hash,
  ) {
    const client = new TelegramClient(
      new sessions.StringSession(stringSession),
      apiId,
      apiHash,
      {
        retryDelay: 5000,
        connectionRetries: 5,
        autoReconnect: true,
      },
    );

    this.connectionManager = new ConnectionManager(client);
    this.groupManager = new GroupManager(client);
    this.messageManager = new MessageManager(client);
    this.chatlistManager = new ChatlistManager(client);
  }

  isConnectionReady() {
    return this.connectionManager.isConnectionReady();
  }

  connect() {
    return this.connectionManager.connect();
  }

  disconnect() {
    return this.connectionManager.disconnect();
  }

  destroy() {
    return this.connectionManager.destroy();
  }

  signIn(phoneNumber: string, phoneCode: string, codeHash: string) {
    return this.connectionManager.signIn(phoneNumber, phoneCode, codeHash);
  }

  start(phoneNumber: string, phoneCode: string) {
    return this.connectionManager.start(phoneNumber, phoneCode);
  }

  sendCode(phoneNumber: string) {
    return this.connectionManager.sendCode(phoneNumber);
  }

  getGroups() {
    return this.groupManager.getGroups();
  }

  sendGroupMessage(groupId: EntityLike, message: string) {
    return this.groupManager.sendGroupMessage(groupId, message);
  }

  sendJoinMessage(title: string) {
    return this.groupManager.sendJoinMessage(title);
  }

  joinGroupByLink(link: string) {
    return this.groupManager.joinGroupByLink(link);
  }

  joinGroupByTitle(groupTitle: string) {
    return this.groupManager.joinGroupByTitle(groupTitle);
  }

  getGroupMessages(groupTitle: string) {
    return this.groupManager.getGroupMessages(groupTitle);
  }

  forwardMessageToGroup(
    messageId: number,
    to: EntityLike,
    from: EntityLike = ADMIN_GROUP.id,
  ) {
    return this.messageManager.forwardMessageToGroup(messageId, from, to);
  }

  forwardMessageToAllGroups(messageId: number) {
    return this.messageManager.forwardMessageToAllGroups(
      messageId,
      ADMIN_GROUP.id,
      [ADMIN_GROUP.title],
    );
  }

  leaveGroup(groupTitle: string) {
    return this.groupManager.leaveGroup(groupTitle);
  }

  joinChatlist(link: string) {
    return this.chatlistManager.joinChatlist(link);
  }

  getChatlist(link: string) {
    return this.chatlistManager.getChatlist(link);
  }

  saveSessionString() {
    return this.connectionManager.saveSessionString();
  }
}
