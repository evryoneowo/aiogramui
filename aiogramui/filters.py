from aiogram.types import Message
from aiogram.enums.chat_type import ChatType

def _to_list(item):
    return item if isinstance(item, list) else [item]

class UserFilter:
    '''Allowed users filter.'''

    def __init__(self, allowed_users: int | list[int]):
        self.allowed_users = _to_list(allowed_users)
    
    def __call__(self, item):
        if isinstance(item, Message):
            chatid = item.chat.id
        else:
            chatid = item.message.chat.id

        return item.from_user.id in self.allowed_users or chat in self.allowed_users

class ChatIdFilter:
    '''Allowed chats filter.'''

    def __init__(self, allowed_chats: int | list[int]):
        self.allowed_chats = _to_list(allowed_chats)
    
    def __call__(self, item):
        if isinstance(item, Message):
            chatid = item.chat.id
        else:
            chatid = item.message.chat.id

        return item.chat.id in self.allowed_chats

class ChatTypeFilter:
    '''Allowed chat types filter.'''

    def __init__(self, allowed_types: ChatType | list[ChatType]):
        self.allowed_types = _to_list(allowed_types)
    
    def __call__(self, item):
        if isinstance(item, Message):
            chattype = item.chat.type
        else:
            chattype = item.message.chat.type

        return chattype in self.allowed_types