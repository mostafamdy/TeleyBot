import asyncio
import os
import random

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


def refresh_data():
    bots = db.get_all()
    online_bots = [bot for bot in bots if bot.message_id]
    return online_bots


async def process_bot(bot):
    print(f"Bot {bot.id} is online.")
    try:
        bot_instance = TelegramBot(bot.session)

        if not bot_instance.is_connected():
            await bot_instance.connect()

        if bot.id not in all_groups:
            all_groups[bot.id] = await bot_instance.get_groups()
        groups = all_groups[bot.id]
        center_group_spam = next(
            (group for group in groups if group.title == SPAM_GROUP.get('title')), None)
        if not center_group_spam:
            print(f"Bot {bot.id} has no spam center group.")

        print(f"Bot {bot.id} found {len(groups)} groups.")

        selected_groups = random.sample(groups, min(5, len(groups)))

        if not selected_groups:
            print(f"Bot {bot.id} has no more groups to process.")
            return

        groups_without_admin = [
            group for group in selected_groups if group.title != ADMIN_GROUP['title']]

        await bot_instance.forward_message_to_group(
            bot.message_id, center_group_spam, ADMIN_GROUP['title']
        )
        tasks = [
            bot_instance.forward_message_to_group(
                bot.message_id, group, ADMIN_GROUP['title'])
            for group in groups_without_admin
        ]
        await asyncio.gather(*tasks)

        print(f"Bot {bot.id} has sent messages to all groups.")
    except Exception as e:
        str_e = str(e)
        print(f"Bot {bot.id} encountered an error: {str_e}")
        if "banned" in str_e:
            await db.update_message_id(bot.id, None)
            print(f"Message for bot ({bot.id}) was reset.")
        if 'deleted' in str_e or 'deactivated' in str_e or 'The key is not registered in the system' in str_e:
            await db.ban(bot.id)
            print(f"Bot {bot.id} was banned.")


async def main():
    while True:
        online_bots = refresh_data()
        if online_bots:
            random.shuffle(online_bots)
            tasks = [process_bot(bot) for bot in online_bots]
            await asyncio.gather(*tasks)
            print("All bots have sent messages.")
        else:
            print("No online bots found.")

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
