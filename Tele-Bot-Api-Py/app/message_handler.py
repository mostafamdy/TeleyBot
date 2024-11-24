import asyncio
from datetime import datetime
import json
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import copy

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

bot_group_status={}
blocked_groups_per_bot = {}

print(len(groups))

for b in bots:
    bot_group_status[b.id]={"AvailableGroups":copy.deepcopy(groups),"VisitedGroups":[]}
    blocked_groups_per_bot[b.id]={"count":0,"groups":[]}

print([b.id for b in bots])

with open("senderSettings.json", "r") as file:
    settings = json.load(file)

def save_blocked_groups():
    # Save to a file
    with open("blocked_groups.json", "w") as file:
        for b in blocked_groups_per_bot.keys():
            blocked_groups_per_bot[b]['count']=len(blocked_groups_per_bot[b]['groups'])
        json.dump(blocked_groups_per_bot, file, indent=4)

async def send_message(breakPointIndex):
    startPoint = int(len(bot_group_status)/working_bots_at_same_time) * breakPointIndex

    _bots = bots[startPoint:]+bots[:startPoint]

    blocked_bots=[]

    while True:
        for bot in _bots:
            save_blocked_groups()
            if bot.id in blocked_bots:
                continue

            start_at = datetime.strptime(bot.start_sending_at, "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - start_at
            working_hours = time_diff.total_seconds() / 3600 
            
            if working_hours>=24:
                db_handler.update_message_id(bot.id,None)
                blocked_bots.append(bot.id)
                continue

            telegram_bot = TelegramBot(bot.session)
            await telegram_bot.connect()

            for _ in range(settings['botMaxMessages']):

                if len(bot_group_status[bot.id]['AvailableGroups']) == 0:
                    bot_group_status[bot.id]['AvailableGroups'] = bot_group_status[bot.id]['VisitedGroups']
                    bot_group_status[bot.id]['VisitedGroups'] = []

                if len(bot_group_status[bot.id]['AvailableGroups'])-1 > 0:
                    random_index = random.randint(0, len(bot_group_status[bot.id]['AvailableGroups'])-1)
                else:
                    random_index = 0

                random_group = bot_group_status[bot.id]['AvailableGroups'].pop(random_index)  
                # date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
                # message = "Bot ("+str(bot.id)+") \ntime "+date_string+"\nmessageID"+str(_)+"\nmessage "+ bot.message
                
                if random_group.id == "-4535626904" or random_group.id == "4535626904":
                    #bot_group_status[bot.id]['VisitedGroups'].append(random_group)
                    continue

                if ( int(random_group.id) < 0 ):
                    ret = await telegram_bot.send_group_message_by_id(int(random_group.id),bot.message_id)
                else:
                    ret = await telegram_bot.send_group_message_by_id(int("-"+random_group.id),bot.message_id)

                if ret != "200":
                    isBanned = await telegram_bot.is_banned()
                    print(f"Bot is Banned ({bot.id}) : {isBanned}")
                    
                    if isBanned:
                        db_handler.ban(bot.id)
                        blocked_bots.append(bot.id)
                        break

                    elif "You're banned from sending messages in supergroups/channels" in ret:
                        blocked_groups_per_bot[bot.id]['groups'].append({"title":random_group.title,"group_id":random_group.id})
                        #print(f"Remove this group \n{random_group.title}\nGroup ID:{random_group.id}")
                        continue
                    
                    elif "You can't write in this chat" in ret:
                        blocked_groups_per_bot[bot.id]['groups'].append({"title":random_group.title,"group_id":random_group.id})
                        #print(f"Remove this group \n{random_group.title}\nGroup ID:{random_group.id}")
                        continue
                    
                    elif "CHAT_SEND_PLAIN_FORBIDDEN" in ret:
                        blocked_groups_per_bot[bot.id]['groups'].append({"title":random_group.title,"group_id":random_group.id})
                        #print(f"Remove this group \n{random_group.title}\nGroup ID:{random_group.id}")
                        continue
                    
                    elif "Could not find the input entity for PeerChannel" in ret:
                        blocked_groups_per_bot[bot.id]['groups'].append({"title":random_group.title,"group_id":random_group.id})
                        print(ret)
                        continue

                    else:
                        print(ret)
                        

                bot_group_status[bot.id]['VisitedGroups'].append(random_group)
                await asyncio.sleep(random.uniform(2,5))
            
working_bots_at_same_time = settings['workingBotsAtSameTime']
# bot will released after 25 message and then 
# message_speed_range from 1 to working bots count if you want more speed add more bots
# NOTE (it's dangerous to use full speed we recomened to use half speed)
if working_bots_at_same_time>len(bot_group_status):
    working_bots_at_same_time=len(bot_group_status)
# Main coroutine
async def main():

    tasks = [send_message(i) for i in range(working_bots_at_same_time)]  # Create 3 async tasks
    await asyncio.gather(*tasks)

asyncio.run(main())

