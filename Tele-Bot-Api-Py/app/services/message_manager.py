from fastapi import HTTPException
from telethon import TelegramClient


class MessageManager:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.from_peer = None

    async def send_message(self,group_id,message):
        try:
            # Search for the group by ID and title
            #group = await self.client.get_entity(group_id)
            #await self.client.send_message(group_id, "message",)
            await self.client.forward_messages(group_id,message,-4535626904)
            return 0
        
        except Exception as e:
             print(e)
             HTTPException(status_code=500, detail={
                "message": "Error sending message",
                "error": str(e)
             })
             return -1

    
    """    async def send_group_message(self, group_title, message):
        try:
            dialogs = await self.client.get_dialogs()
            group = next(
                (dialog for dialog in dialogs if dialog.title == group_title), None)
            if not group:
                HTTPException(status_code=404, detail={
                    "message": "Group not found"
                })
            me = await self.client.get_me()
            group_message = message if message else f'Hello, I am {me.first_name}'
            await self.client.send_message(group, group_message)
            return {'message': 'Message sent successfully'}
        except Exception as e:
            HTTPException(status_code=500, detail={
                "message": "Error sending message",
                "error": str(e)
            })
    """
    async def forward_message_to_group(self, message_id, to, from_: str):
        try:
            if not self.from_peer:
                dialogs = await self.client.get_dialogs()
                group = next(
                    (dialog for dialog in dialogs if dialog.title == from_), None)
                if not group:
                    HTTPException(status_code=404, detail={
                        "message": "Group not found"
                    })
                self.from_peer = group

            print(f"Forwarding message to {to.title}")
            await self.client.forward_messages(to, message_id, self.from_peer.id)
            print(f"Message was forwarded to {to.title}")
        except Exception as e:
            print(str(e))
            raise Exception(f"Error forwarding message to group: {str(e)}")

    async def forward_message_to_all_groups(self, message_id, from_, group_titles):
        try:
            for group_title in group_titles:
                group = await self.client.get_entity(group_title)
                await self.forward_message_to_group(message_id, from_, group)
        except Exception as e:
            HTTPException(status_code=500, detail={
                "message": "Error forwarding message",
                "error": str(e)
            })

    async def get_last_message_id(self):
        messages = await self.client.get_messages(-4535626904, limit=1)
        if messages:
            last_message_id = messages[0].id
            return last_message_id
        else:
            return None