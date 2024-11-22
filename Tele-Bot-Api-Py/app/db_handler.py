from datetime import datetime
from fastapi import HTTPException

try:
    from app.models.database import Bot, BannedBot,GroupsData, SessionLocal
except ImportError:
    from models.database import Bot, BannedBot,GroupsData, SessionLocal


class DbHandler:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self):
        try:
            self.db = SessionLocal()
            return self.db.query(Bot).all()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get all bots: {str(e)}")
        finally:
            self.db.close()

    def get_all_banned(self):
        try:
            self.db = SessionLocal()
            return self.db.query(BannedBot).all()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get all banned bots: {str(e)}")
        finally:
            self.db.close()

    def get_all_groups(self):
        try:
            self.db = SessionLocal()
            return self.db.query(GroupsData).all()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get all banned bots: {str(e)}")
        finally:
            self.db.close()
    
    def add_group(self,link,id,title):
        try:
            self.db = SessionLocal()
            groupData = GroupsData(link=link,id=id,title=title)
            self.db.add(groupData)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to add bot: {str(e)}")
        finally:
            self.db.close()

    def add(self, session: str, phone: str):
        try:
            self.db = SessionLocal()
            bot = Bot(session=session, phone=phone)
            self.db.add(bot)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to add bot: {str(e)}")
        finally:
            self.db.close()

    def delete(self, id: int):
        try:
            self.db = SessionLocal()
            bot = self.db.query(Bot).filter(Bot.id == id).first()
            if bot:
                self.db.delete(bot)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to delete bot: {str(e)}")
        finally:
            self.db.close()

    def deleteGroup(self, id: str):
        try:
            self.db = SessionLocal()
            g = self.db.query(GroupsData).filter(GroupsData.id == id).first()
            if g:
                self.db.delete(g)
                self.db.commit()
                return 0
            else:
                return -1
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to delete group: {str(e)}")
        finally:
            self.db.close()

    def get(self, id: int):
        try:
            self.db = SessionLocal()
            return self.db.query(Bot).filter(Bot.id == id).first()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get bot by ID: {str(e)}")
        finally:
            self.db.close()

    def get_bots_have_message(self):
        try:
            self.db = SessionLocal()
            return self.db.query(Bot).filter(Bot.message != None)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get bot by ID: {str(e)}")
        finally:
            self.db.close()


    def get_by_phone(self, phone: str):
        try:
            self.db = SessionLocal()
            bot = self.db.query(Bot).filter(Bot.phone == phone).first()
            if bot:
                return bot
            return self.db.query(BannedBot).filter(BannedBot.phone == phone).first()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get bot by phone: {str(e)}")
        finally:
            self.db.close()

    def update_message(self, id: int, message: str):
        try:
            self.db = SessionLocal()
            bot = self.db.query(Bot).filter(Bot.id == id).first()
            if bot:
                bot.message = message
                bot.start_sending_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to update message ID: {str(e)}")
        finally:
            self.db.close()

    def ban(self, id: int):
        try:
            self.db = SessionLocal()
            bot = self.db.query(Bot).filter(Bot.id == id).first()
            if bot:
                self.db.delete(bot)
                banned_bot = BannedBot(
                    phone=bot.phone, bot_created_at=bot.created_at,session=bot.session)
                self.db.add(banned_bot)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to ban bot: {str(e)}")
        finally:
            self.db.close()
