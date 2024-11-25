from telethon import TelegramClient
from telethon.sessions import StringSession

try:
    from app.constants import API, ADMIN_GROUP
    from app.services.connection_manager import ConnectionManager
    from app.services.group_manager import GroupManager
    from app.services.message_manager import MessageManager
    from app.services.chatlist_manager import ChatlistManager
except ModuleNotFoundError:
    from constants import API, ADMIN_GROUP
    from services.connection_manager import ConnectionManager
    from services.group_manager import GroupManager
    from services.message_manager import MessageManager
    from services.chatlist_manager import ChatlistManager

class ProxyData:
    def __init__(self,ip,username,password) -> None:
        self.ip=ip
        self.username=username
        self.password=password
        self.location=""

class TelegramBot:
    def __init__(self, string_session='', api_id=API['id'], api_hash=API['hash'],proxy=None):
        if proxy is not None:

            client = TelegramClient(
                session=StringSession(string_session),
                api_id=api_id,
                api_hash=api_hash,
                retry_delay=5,
                auto_reconnect=True,
                timeout=20,
                proxy=(proxy.ip,proxy.port)
            ) 

        else:
            client = TelegramClient(
                session=StringSession(string_session),
                api_id=api_id,
                api_hash=api_hash,
                retry_delay=5,
                auto_reconnect=True,
                timeout=20,
            )
        self.connection_manager = ConnectionManager(client)
        self.group_manager = GroupManager(client)
        self.message_manager = MessageManager(client)
        self.chatlist_manager = ChatlistManager(client)

    def is_connected(self):
        return self.connection_manager.is_connected()

    def connect(self):
        return self.connection_manager.connect()

    def disconnect(self):
        return self.connection_manager.disconnect()

    def start(self, phone_number, phone_code):
        return self.connection_manager.start(phone_number, phone_code)

    def sign_in(self, phone_number, phone_code, phone_code_hash=None):
        return self.connection_manager.sign_in(phone_number, phone_code, phone_code_hash)

    def send_code(self, phone_number):
        return self.connection_manager.send_code(phone_number)

    def rename(self, first_name, last_name=""):
        return self.connection_manager.rename_bot(first_name, last_name)

    def is_banned(self):
        return self.connection_manager.is_banned()

    def get_group_by_title(self, group_title):
        return self.group_manager.get_group_by_title(group_title)

    def get_groups(self):
        return self.group_manager.get_groups()
    
    def get_group_link_from_id(self,groupID):
        # must be admin of group
        return self.group_manager.get_group_link_from_id(groupID)

    def send_group_message(self, group_title: str, message: str | None = None):
        return self.message_manager.send_group_message(group_title, message)

    def join_group(self, link):
        return self.group_manager.join_group(link)

    def join_group_by_id(self, group_title):
        return self.group_manager.join_group_by_id(group_title)

    def get_group_messages(self, group_title):
        return self.group_manager.get_group_messages(group_title)

    def forward_message_to_group(self, message_id, to, from_):
        return self.message_manager.forward_message_to_group(message_id, to, from_)

    def forward_message_to_all_groups(self, message_id):
        return self.message_manager.forward_message_to_all_groups(
            message_id, ADMIN_GROUP['id'], [ADMIN_GROUP['title']]
        )
    def send_group_message_by_id(self,groupID,messageID,botID=None):
        self.message_manager.send_message(group_id=groupID,message=messageID)
        print(f"{botID} Message sent Group ID {groupID}")
        return 
    
    def leave_group(self, group_title):
        return self.group_manager.leave_group(group_title)
    
    def get_group_info_by_link(self,link):
       return self.group_manager.get_group_info_from_link(link)
    
    def join_chatlist(self, link):
        return self.chatlist_manager.join_chatlist(link)

    def get_chatlist(self, link):
        return self.chatlist_manager.get_chatlist(link)

    def save_session_string(self):
        return self.connection_manager.save_session_string()
    
    def get_last_message_id(self):
        return self.message_manager.get_last_message_id()
