from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest as JoinChannel


class ChatlistManager:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def join_chatlist(self, link):
        await self.client(JoinChannel(link))

    async def get_chatlist(self, link):
        group = await self.client.get_entity(link)
        return await self.client.get_participants(group)
