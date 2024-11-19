export type Bot = {
  id: number;
  session: string;
  phone: string;
  messageId: number;
  joinedDate: string;
};

export type BannedBot = {
  id: number;
  phone: string;
  bannedDate: string;
  joinedDate: string;
};
