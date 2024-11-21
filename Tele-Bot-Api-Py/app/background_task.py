import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
lock=False

class AsyncEventHandler(FileSystemEventHandler):
    def __init__(self, loop, callback):
        self.loop = loop
        self.callback = callback

    async def on_modified_async(self, event):
        if not event.is_directory:
            await self.callback(event.src_path)

    def on_modified(self, event):
        # Schedule the async task in the event loop
        asyncio.run_coroutine_threadsafe(self.on_modified_async(event), self.loop)

async def file_modified_callback(file_path):   
    if globals()['lock']:
        pass
    
    elif "bots.db" == file_path.split("\\")[-1].strip():
        globals()['lock']=True
        #print(f"Database modified ")
        # Add additional async actions here
        print("Database has changed!")
        db_bot = db_handler.get_bots_have_message()
        db_group = db_handler.get_all_groups()
        
        for bot in db_bot:
            telegram_bot = TelegramBot(bot.session)
            await telegram_bot.connect()
            for group in db_group:
                await telegram_bot.send_group_message_by_id(int("-"+group.id), bot.message)
            db_handler.update_message(id=bot.id,message=None)
            await telegram_bot.disconnect()
        globals()['lock']=False


async def monitor_directory(path):
    loop = asyncio.get_running_loop()
    event_handler = AsyncEventHandler(loop, file_modified_callback)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            await asyncio.sleep(30)  # Keep the coroutine alive
    finally:
        observer.stop()
        observer.join()

# Run the async directory monitor
path_to_watch = "./"  # Replace with your directory
asyncio.run(monitor_directory(path_to_watch))
