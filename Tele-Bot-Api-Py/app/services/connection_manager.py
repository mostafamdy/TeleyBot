from fastapi import HTTPException
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest


class ConnectionManager:
    def __init__(self, client: TelegramClient):
        self.client = client

    def is_connected(self):
        return self.client.is_connected()

    async def is_banned(self):
        try:
            print(await self.client.get_me())
            return False
        except Exception as e:
            print(e)
            return True

    async def connect(self):
        try:
            await self.client.connect()
        except Exception as e:
            print(e)
            raise Exception(f"Error connecting to Telegram: {str(e)}")

    async def disconnect(self):
        try:
            await self.client.disconnect()
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error disconnecting from Telegram",
                "error": str(e)
            })

    async def start(self, phone_number, phone_code):
        try:
            await self.client.start(phone=phone_number)
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error starting Telegram client",
                "error": str(e)
            })

    async def send_code(self, phone_number):
        try:
            return await self.client.send_code_request(phone_number)
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error sending code to phone number",
                "error": str(e)
            })

    async def sign_in(self, phone_number, phone_code, phone_code_hash=None):
        try:
            return await self.client.sign_in(phone=phone_number, code=phone_code, phone_code_hash=phone_code_hash)
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error signing in to Telegram",
                "error": str(e)
            })

    async def get_entity(self, entity):
        try:
            return await self.client.get_entity(entity)
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error getting entity",
                "error": str(e)
            })

    async def rename_bot(self, first_name, last_name=""):
        try:
            await self.client(UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error renaming bot",
                "error": str(e)
            })

    def save_session_string(self):
        return self.client.session.save()
