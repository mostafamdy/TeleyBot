import asyncio
from datetime import datetime
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
try:
    from app.constants import ADMIN_GROUP
    from app.db_handler import DbHandler
    from app.services.telegram_bot import TelegramBot
except ImportError:
    from constants import ADMIN_GROUP
    from db_handler import DbHandler
    from services.telegram_bot import TelegramBot

# Database path
DB_PATH = "bots.db"
db_handler = DbHandler()

bots = db_handler.get_bots_have_message()
groups = db_handler.get_all_groups()

groups_status={}
for b in bots:
    groups_status[b.id]={"AvailableGroups":groups,"VisitedGroups":[]}
print([b.id for b in bots])
"""
3 

1 - - - - 1 - - - - 1 - - - -

bots/3


"""
async def send_message(breakPointIndex):
    startPoint = int(len(groups_status)/working_bots_at_same_time) * breakPointIndex

    _bots = bots[startPoint:]+bots[:startPoint]
    print(startPoint)
    print([b.id for b in _bots])
    print(len(_bots))

    while True:
        for bot in _bots:
            
            telegram_bot = TelegramBot(bot.session)
            await telegram_bot.connect()
            for _ in range(25):
                if len(groups_status[bot.id]['AvailableGroups']) == 0:
                    groups_status[bot.id]['AvailableGroups'] = groups_status[bot.id]['VisitedGroups']
                    groups_status[bot.id]['VisitedGroups'] = []
                
                try:
                    random_index = random.randint(0, len(groups_status[bot.id]['AvailableGroups'])-1)
                except:
                    random_index = 0

                random_group = groups_status[bot.id]['AvailableGroups'].pop(random_index)  
                
                date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
                #print(date_string)
                print("\nBot ("+str(bot.id)+") \ntime "+date_string+"\nmessage "+ bot.message+"\n")

                #await telegram_bot.send_group_message_by_id(int("-"+random_group.id), "Bot ("+str(bot.id)+") \ntime "+date_string+"\nmessageID"+str(_)+"\nmessage "+ bot.message)
                
                groups_status[bot.id]['VisitedGroups'].append(random_group)

                print(f"{bot.id} groups visited {len(groups_status[bot.id]['VisitedGroups'])}")
                print(f"{bot.id} groups available {len(groups_status[bot.id]['AvailableGroups'])}")
                #await asyncio.sleep(random.uniform(3,5))



working_bots_at_same_time = 2

# Main coroutine
async def main():
    tasks = [send_message(i) for i in range(working_bots_at_same_time)]  # Create 3 async tasks
    await asyncio.gather(*tasks)

asyncio.run(main())