import asyncio
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

# Connected bots
# bots_groups = {botid:{AvailableGroups:[],VisitedGroups:[]}}
bots_groups={}
async def send_message(index):
    for bot in bots:
        telegram_bot = TelegramBot(bot.session)
        await telegram_bot.connect()
        for i in range(25):
            bots_groups[bot.id]['AvailableGroups']
            for group in groups:
                await telegram_bot.send_group_message_by_id(int("-"+group.id), bot.message)

#db_handler.update_message(id=bot.id,message=None)
#await telegram_bot.disconnect()


"""
1- Read database thread
2- sending messages thread
working bots at the same time 2
"""

working_bots_at_same_time = 2


import threading
import time

# Function to run in a thread
def database_handler():
    while True:
        pass
        # get groups
        # get bots massages
        time.sleep(5)


database_listener = threading.Thread(target=database_handler, args=())
threads=[]

for i in range(working_bots_at_same_time):
    _thread = threading.Thread(target=send_message, args=(i))
    threads.append(_thread)
    _thread.start()

# Start threads
database_listener.start()

# Wait for threads to complete
database_listener.join()

for t in threads:
    t.join()




import asyncio

# An asynchronous function
async def async_task(task_id):
    print(f"Async task {task_id} started.")
    await asyncio.sleep(2)
    print(f"Async task {task_id} finished.")

# Main coroutine
async def main():
    tasks = [async_task(i + 1) for i in range(3)]  # Create 3 async tasks
    await asyncio.gather(*tasks)

asyncio.run(main())





