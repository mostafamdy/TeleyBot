import asyncio
import os
import random
import sys
from contextlib import suppress

try:
    from app.constants import ADMIN_GROUP, SPAM_GROUP,TELEGRAM_LINKS
    from app.services.telegram_bot import TelegramBot
    from app.db_handler import DbHandler
except ImportError:
    from constants import ADMIN_GROUP, SPAM_GROUP,TELEGRAM_LINKS
    from services.telegram_bot import TelegramBot
    from db_handler import DbHandler


class AbsoluteSilence:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

all_groups = {}
db = DbHandler()


def refresh_data():
    bots = db.get_all()
    online_bots = [bot for bot in bots if bot.message_id]
    return online_bots


async def process_bot(bot):
    #print(f"Bot {bot.id} is online.")
    try:
        bot_instance = TelegramBot(bot.session)
        #if not bot_instance.is_connected():
        await bot_instance.connect()
        selected_groups = random.sample(TELEGRAM_LINKS,10)
        await bot_instance.forward_message_to_group(
            bot.message_id, "https://t.me/+2VTvorWtrbg2NTdi", ADMIN_GROUP['link'])
        tasks = [
            bot_instance.forward_message_to_group(
                bot.message_id, group, ADMIN_GROUP['link'])
            for group in selected_groups
        ]
        await asyncio.gather(*tasks)

        #print(f"Bot {bot.id} has sent messages to all groups.")
        await bot_instance.disconnect()
    except Exception as e:
        str_e = str(e)
        #print(f"Bot {bot.id} encountered an error: {str_e}")
        if 'deleted' in str_e or 'deactivated' in str_e or 'The key is not registered in the system' in str_e:
            await db.ban(bot.id)
            print(f"Bot {bot.id} was banned.")
        
        pass


async def main():
    #with AbsoluteSilence():
        #with suppress(Exception):
            online_bots = refresh_data()
            if online_bots:
                random.shuffle(online_bots)
                for i in range(0, len(online_bots), 1000):
                    batch = online_bots[i:i + 1000]
                    tasks = [process_bot(bot) for bot in batch]
                    await asyncio.gather(*tasks)
                    print(f"Batch {i // 1000 + 1} of bots have sent msesages.")
                print("All bots have sent messages.")
            else:
                print("No online bots found.")
            
            os.system("pm2 restart 3 --update-env")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(f"Script terminated by user: {str(e)}")
        os.system("pm2 restart 3 --update-env")
    except Exception as e:
        print(f"Script encountered an error: {str(e)}")
        print("Script terminated.")
        os.system("pm2 restart 3 --update-env")
