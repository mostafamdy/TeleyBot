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

bots_groups={}
for b in bots:
    bots_groups[b.id]={"AvailableGroups":groups,"VisitedGroups":[]}

"""
3 

1 - - - - 1 - - - - 1 - - - -

bots/3


"""
async def send_message(breakPointIndex):
    startPoint = int(len(bots_groups)/working_bots_at_same_time) * breakPointIndex

    _bots = bots[startPoint:]+bots[:startPoint]
    print(startPoint)
    print(_bots)
    
    while True:
        for bot in _bots:
            telegram_bot = TelegramBot(bot.session)
            await telegram_bot.connect()
            for i in range(25):
                av_groups = bots_groups[bot.id]['AvailableGroups']
                if len(av_groups) == 0:
                    bots_groups[bot.id]['AvailableGroups'] = bots_groups[bot.id]['VisitedGroups']
                    bots_groups[bot.id]['VisitedGroups'] = []
                    av_groups = bots_groups[bot.id]['AvailableGroups']
                if len(av_groups) == 1:
                    print(f"available group lens is 1")
                    random_index = 0
                else:
                    print(f"Else available group lens is {len(av_groups)}")
                    random_index = random.randint(0, len(av_groups)-1)

                random_group = bots_groups[bot.id]['AvailableGroups'].pop(random_index)  
                date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
                print(date_string)
                print("Bot ("+str(bot.id)+") \ntime "+date_string+"\nmessage "+ bot.message)

                await telegram_bot.send_group_message_by_id(int("-"+random_group.id), "Bot ("+str(bot.id)+") \ntime "+date_string+"\nmessage "+ bot.message)
                bots_groups[bot.id]['VisitedGroups'].append(random_group)

                await asyncio.sleep(random.uniform(3,5))



working_bots_at_same_time = 4

# Main coroutine
async def main():
    tasks = [send_message(i) for i in range(working_bots_at_same_time)]  # Create 3 async tasks
    await asyncio.gather(*tasks)

asyncio.run(main())