from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.chatlists import JoinChatlistInviteRequest, CheckChatlistInviteRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

class GroupManager:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def get_group_info_from_link(self,group_link):
        try:
            # Fetch the group entity from the link
            entity = await self.client.get_entity(group_link)
            # Print or return the group ID
            # print("Group ID:", entity.id)
            return {"id" : entity.id, "title" : entity.title}
        except Exception as e:
            print("An error occurred:", e)

    async def get_group_link_from_id(self,groupID):
         try:
            link = await self.client(ExportChatInviteRequest(groupID))
            return link.link
         except Exception as e:
            print("Failed to retrieve invite link:", e)

    async def get_groups(self):
        try:
            dialogs = await self.client.get_dialogs()
            print(len(dialogs))
            dialogs_list = [
                dialog for dialog in dialogs if dialog.is_group]
            return list(dialogs_list)
        except Exception as e:
            raise Exception(f"Error getting groups: {str(e)}")

    async def get_group_by_title(self, group_title):
        dialogs = await self.client.get_dialogs()
        group = next(
            (dialog for dialog in dialogs if dialog.title == group_title), None)
        return group

    async def join_group(self, link):
        hash_part = link.split('/')[-1].replace('+', '')

        if ('addlist' in link):
            chatlist = await self.client(CheckChatlistInviteRequest(hash_part))
            peers = [chat.id for chat in chatlist.chats]
            await self.client(JoinChatlistInviteRequest(hash_part, peers))
            return {'message': 'Chatlist joined successfully'}
        else:
            await self.client(ImportChatInviteRequest(hash_part))
            return {'message': 'Group joined successfully'}

    async def join_group_by_id(self, group_title):
        group = await self.client.get_entity(group_title)
        await self.client(JoinChannelRequest(group))

    async def get_group_messages(self, group_title):
        group = await self.client.get_entity(group_title)
        return await self.client.get_messages(group)

    async def leave_group(self, group_title):
        group = await self.client.get_entity(group_title)
        await self.client(LeaveChannelRequest(group))
