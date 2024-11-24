import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from fastapi import APIRouter
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse

try:
    from app.services.telegram_bot import TelegramBot
    from app.db_handler import DbHandler
except ImportError:
    from services.telegram_bot import TelegramBot
    from db_handler import DbHandler

router = APIRouter()
db_handler = DbHandler()


class UpdateMessageId(BaseModel):
    start: int
    end: int


@router.get("/")
def get_bots():

    return {'data': db_handler.get_all()}


@router.get("/count/")
def get_bots_count():
    bots = db_handler.get_all()
    available_bots = [bot for bot in bots if not bot.message_id]
    unavailable_bots = [bot for bot in bots if bot.message_id]
    banned_bots = db_handler.get_all_banned()

    return {
        'data': {
            'available': len(available_bots),
            'unavailable': len(unavailable_bots),
            'banned': len(banned_bots)
        }
    }


@router.get("/banned/")
def get_banned_bots():
    banned_bots = db_handler.get_all_banned()
    return {'data': banned_bots}


@router.put("/messages/{message_id}")
def update_message_id(message_id: int, update_data: UpdateMessageId):
    try:
        bots = db_handler.get_all()[update_data.start-1:update_data.end]
        for bot in bots:
            db_handler.update_message_id(bot.id, message_id)
        return {"message": "message updated"}
    except Exception as e:
        return {"message": 'Error updating message_id', 'error': str(e)}


class Message(BaseModel):
    start: int
    end: int
    messageID:int

@router.post("/sendMessage/")
async def send_message(message:Message):
    try:
        bots = db_handler.get_all()[message.start-1:message.end]
        last_message_id = None
        for bot in bots:
            bot_client = TelegramBot(bot.session)
            try:
                # await bot_client.connect()
                last_message_id = await bot_client.get_last_message_id()
                # db_handler.update_message_id(bot.id, last_message_id)
                # await bot_client.disconnect()
                
            except Exception as e:
                print(f"ERROR {bot.id}\n {e}")
                continue
        
        if last_message_id is None:
            return {"message": "can't send this message check bots count"}
        
        os.system("sudo systemctl restart massage")
        return {"message": "message sent"}
    
    except Exception as e:
        return {"message": 'Error updating message_id', 'error': str(e)}

@router.get("/stopSending/")
def stop_sending():
    try:
        bots = db_handler.get_all()
        for bot in bots:
            db_handler.update_message_id(bot.id, None)
        os.system("sudo systemctl restart massage")
        return {"message": "message sent"}
    except Exception as e:
        return {"message": 'Error updating message_id', 'error': str(e)}


@router.delete("/{bot_id}/")
def delete_bot(bot_id: int):
    db_handler.delete(bot_id)
    return {"message": "bot deleted"}


@router.get("/groups/")
async def get_bot_groups():
    bots = db_handler.get_all()
    bots_with_groups = []

    async def process_bot(bot):
        try:
            bot_client = TelegramBot(bot.session)
            await bot_client.connect()
            groups = await bot_client.get_groups()
            bots_with_groups.append({
                "id": bot.id,
                "phone": bot.phone,
                "group_count": len(groups)
            })
            await bot_client.disconnect()
        except Exception as e:
            bots_with_groups.append({
                "id": bot.id,
                "phone": bot.phone,
                "error": str(e)
            })

    def process_bot_sync(bot):
        return asyncio.run(process_bot(bot))

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        futures = [loop.run_in_executor(
            executor, process_bot_sync, bot) for bot in bots]
        await asyncio.gather(*futures)

    return {"data": bots_with_groups}


@router.get("/groups/{bot_id}/")
async def get_bot_groups(bot_id: int):
    try:
        bot = db_handler.get(bot_id)
        bot_client = TelegramBot(bot.session)
        await bot_client.connect()
        groups = await bot_client.get_groups()
        await bot_client.disconnect()
        return {"data": {
            "groups count": len(groups),
        }}
    except Exception as e:
        return {"message": 'Error retrieving groups', 'error': str(e)}


@router.get("/rename/")
async def rename_bot(bot_id: int):
    try:
        bot = db_handler.get(bot_id)
        bot_client = TelegramBot(bot.session)
        await bot_client.connect()
        await bot_client.rename(f'dc{bot.id}')
        await bot_client.disconnect()
        return {"message": "bot renamed"}
    except Exception as e:
        return {"message": 'Error renaming bot', 'error': str(e)}


@router.get("/rename/all")
async def rename_all_bots(first_name: str = 'dc'):
    bots = db_handler.get_all()
    errors = []

    async def process_bot(bot):
        try:
            bot_client = TelegramBot(bot.session)
            await bot_client.connect()
            await bot_client.rename(f'{first_name}{bot.id}')
            await bot_client.disconnect()
        except Exception as e:
            errors.append({
                "id": bot.id,
                "phone": bot.phone,
                "error": str(e)
            })

    try:
        await asyncio.gather(*(process_bot(bot) for bot in bots))
    except Exception as e:
        return {"message": 'Error renaming bots', 'error': str(e)}

    if errors:
        return {"message": 'Error renaming bots', 'errors': errors}

    return {"message": "bots renamed"}


@router.post("/ban/")
def ban_bot(bot_id: int, phone: str):
    db_handler.ban(bot_id, phone)
    return {"message": "bot banned"}

class SenderSettings(BaseModel):
    workingBotsAtSameTime: int
    botMaxMessages: int


@router.post("/settings/change")
def save_settings(settings:SenderSettings):
    try:
        data = {
        "workingBotsAtSameTime":settings.workingBotsAtSameTime ,
        "botMaxMessages": settings.botMaxMessages
        }
        # Save to a file
        with open("senderSettings.json", "w") as file:
            json.dump(data, file, indent=4)
        os.system("sudo systemctl restart massage")
        return {"message":"Settings Updated"}
    except:
        return {"message":"Can't change the settings now"}

@router.get("/settings/")
def set_settings():
    # Load existing JSON
    with open("senderSettings.json", "r") as file:
        settings = json.load(file)
    
    return JSONResponse(content=settings)

    