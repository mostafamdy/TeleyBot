from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
try:
    from app.constants import ADMIN_GROUP
    from app.db_handler import DbHandler
    from app.services.telegram_bot import TelegramBot
except ImportError:
    from constants import ADMIN_GROUP
    from db_handler import DbHandler
    from services.telegram_bot import TelegramBot

router = APIRouter()
db_handler = DbHandler()


@router.get("/")
async def get_groups():
    try:
        db_bot = db_handler.get_all()[0]
        telegram_bot = TelegramBot(db_bot.session)
        await telegram_bot.connect()
        chatlist_groups = await telegram_bot.get_groups()
        
        print(f"groups count: {len(chatlist_groups)}")
        print(f"{chatlist_groups[1].id}\t {chatlist_groups[1].title}")
        titles = [group.title for group in chatlist_groups]
        await telegram_bot.disconnect()

        return {
            'data': titles,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "message": "Error getting groups",
            "error": str(e)
        }) 


@router.get("/get_groups")
async def get_groups():
    try:
        _groups = db_handler.get_all_groups()
        groups = [{"title":group.title,"id":group.id,"link":group.link} for group in _groups]

        return groups
        
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "message": "Error getting groups",
            "error": str(e)
        })
    

@router.get("/deleteGroup")
async def deleteGroup(id):
    try:
        _statue = db_handler.deleteGroup(id)
        if _statue==-1:
            return {"message":"Wrong ID"}
        
        return {"message": "Group is deleted"}
    except Exception as e:
        print(e)
  
@router.post("/join/")
async def join_group(link: str, bot_id: int):
    try:
        db_bot = db_handler.get(bot_id)
        telegram_bot = TelegramBot(db_bot.session)
        await telegram_bot.connect()
        result = await telegram_bot.join_group(link)
        await telegram_bot.disconnect()
        return {"message": result.get('message')}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "message": "Error joining group",
            "error": str(e)
        })

class JoinGroupALL(BaseModel):
    link:str

@router.post("/join/all")
async def join_group(data: JoinGroupALL):
    """
    1- get all bots seasions
    2- loop to connect bots and join group
    3- if it first bot get group info (id title) and save it in database
    """
    try:
        db_bot = db_handler.get_all()
        print("All bots", len(db_bot))

        for indx,bot in enumerate(db_bot):
            telegram_bot = TelegramBot(bot.session)
            # connect
            try:
                await telegram_bot.connect()
            except Exception as e:
                print(e)
                continue
            # Join Group
            try:
                result = await telegram_bot.join_group(data.link)
                # Save Group
                if indx == 0:
                    info = await telegram_bot.get_group_info_by_link(data.link)
                    db_handler.add_group(data.link,info['id'],info['title'])

                await telegram_bot.disconnect()
            except Exception as e:
                print(e)
                continue
        
        return {"message": result.get('message')}
    
    except Exception as e:
        print(e)
    finally:
        return {"message": "All bots joined group"}


@router.post("/join/all/list/")
async def join_groups_list(data: JoinGroupALL):
    try:
        db_bot = db_handler.get_all()
        print("All bots", len(db_bot))
        for indx,bot in enumerate(db_bot):
            telegram_bot = TelegramBot(bot.session)
            try:
                await telegram_bot.connect()
            except Exception as e:
                print(e)
                continue
            # Join Groups
            try:
                if indx == 0:
                    # Save Groups
                    groups_before = await telegram_bot.get_groups()
                    groups_before = [g.title for g in groups_before]
                    result = await telegram_bot.join_group(data.link)
                    groups_after = await telegram_bot.get_groups()
                    for group in groups_after:
                        if group.title in groups_before:
                            continue
                        #info = await telegram_bot.get_group_info_by_link(data.link)
                        db_handler.add_group(None,group.id,group.title)

                else:
                    result = await telegram_bot.join_group(data.link)
                await telegram_bot.disconnect()
            except Exception as e:
                print(e)
                continue
        
        return {"message": result.get('message')}
    
    except Exception as e:
        print(e)
    finally:
        return {"message": "All bots joined group"}


@router.get("/send-message/")
async def send_group_message(bot_id: int):
    try:
        db_bot = db_handler.get(bot_id)
        telegram_bot = TelegramBot(db_bot.session)
        await telegram_bot.connect()
        await telegram_bot.send_group_message('Spam center dont', 'test')
        await telegram_bot.disconnect()
        return {"message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "message": "Error sending message",
            "error": str(e)
        })


@router.get("/forward-message/")
async def forward_message_to_group(message_id: int, bot_id: int):
    try:
        db_bot = db_handler.get(bot_id)
        telegram_bot = TelegramBot(db_bot.session)
        if not telegram_bot.is_connected():
            await telegram_bot.connect()

        to = await telegram_bot.get_group_by_title('Spam center dont')
        if not to:
            print(f"Group not found")
            raise HTTPException(status_code=404, detail={
                "message": "Group not found"
            })
        await telegram_bot.forward_message_to_group(message_id, to, ADMIN_GROUP.get('title'))
        await telegram_bot.disconnect()
        return {"message": "Message forwarded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "message": "Error forwarding message",
            "error": str(e)
        })
