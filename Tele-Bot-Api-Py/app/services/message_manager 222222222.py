from fastapi import HTTPException
from telethon import TelegramClient


class MessageManager:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.from_peer = None

    async def send_group_message(self, group_title, message):
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

    async def forward_message_to_group(self, message_id, to, from_: str):
        try:
            await self.client.forward_messages(to, message_id,from_)
        except Exception as e:
            # print(str(e))
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
