import asyncio
from datetime import datetime
import json
import os
import random
import copy

try:
    from app.constants import ADMIN_GROUP, SPAM_GROUP
    from app.services.telegram_bot import TelegramBot
    from app.db_handler import DbHandler
except ImportError:
    from constants import ADMIN_GROUP, SPAM_GROUP
    from services.telegram_bot import TelegramBot
    from db_handler import DbHandler

all_groups = {}
db = DbHandler()

bots = db.get_bots_have_message()
groups = db.get_all_groups()

bot_group_status={}
blocked_groups_per_bot = {}

for b in bots:
    bot_group_status[b.id]={"AvailableGroups":copy.deepcopy(groups),"VisitedGroups":[]}
    blocked_groups_per_bot[b.id]={"count":0,"groups":[]}

with open("senderSettings.json", "r") as file:
    settings = json.load(file)

working_bots_at_same_time = settings['workingBotsAtSameTime']

if working_bots_at_same_time>len(bot_group_status):
    working_bots_at_same_time=len(bot_group_status)


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
        if len(blocked_bots)==len(_bots):
            break

        for bot in _bots:
            if bot.id in blocked_bots:
                continue
                
            start_at = datetime.strptime(bot.start_sending_at, "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - start_at
            working_hours = time_diff.total_seconds() / 3600 
            
            if working_hours>=24:
                db.update_message_id(bot.id,None)
                blocked_bots.append(bot.id)
                continue

            if len(bot_group_status[bot.id]['AvailableGroups']) == 0:
                bot_group_status[bot.id]['AvailableGroups'] = bot_group_status[bot.id]['VisitedGroups']
                bot_group_status[bot.id]['VisitedGroups'] = []

            bot_instance = TelegramBot(bot.session)
            try:
                if not bot_instance.is_connected():
                    await bot_instance.connect()
            
            except Exception as e:
                isBanned = await bot_instance.is_banned()
                print(f"Bot is Banned ({bot.id}) : {isBanned}")
                if isBanned:
                    db.ban(bot.id)
                    blocked_bots.append(bot.id)
                    continue

            botGroups =  bot_group_status[bot.id]['AvailableGroups'] 
            selected_groups = random.sample(botGroups, min(settings['botMaxMessages'], len(botGroups)))
            
            print(selected_groups)
            
            if not selected_groups:
                print(f"Bot {bot.id} has no more groups to process.")
                continue

            for g in selected_groups:
                gi = bot_group_status[bot.id]['AvailableGroups'].index(g)
                bot_group_status[bot.id]['AvailableGroups'].pop(gi)
                bot_group_status[bot.id]['VisitedGroups'].append(g)  
            
            groups_to_send = [
                    group for group in selected_groups if group.id not in ["-4535626904","4535626904"]]
                
            groups_to_send = [-1*abs(int(g.id)) for g in groups_to_send]
                

            try:
                tasks = [
                    bot_instance.send_group_message_by_id(
                        group_id , bot.message_id)
                    for group_id in groups_to_send
                ]
                
                await asyncio.gather(*tasks)

                print(f"Bot {bot.id} has sent messages to all groups.")
            
            except Exception as e:
                str_e = str(e)
                print(e)
                isBanned = await bot_instance.is_banned()
                
                print(f"Bot is Banned ({bot.id}) : {isBanned}")
                if isBanned:
                    db.ban(bot.id)
                    blocked_bots.append(bot.id)
                    continue


async def main():
    random.shuffle(bots)
    tasks = [send_message(i) for i in range(working_bots_at_same_time)]
    await asyncio.gather(*tasks)
    print("All bots have sent messages.")



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(f"Script terminated by user: {str(e)}")
        os.system("sudo systemctl restart massage")
    except Exception as e:
        print(f"Script encountered an error: {str(e)}")
        print("Script terminated.")
        os.system("sudo systemctl restart massage")
