# custom.py | part of aiogramui framework
# author: evryoneowo | year: 2025
# github: https://github.com/evryoneowo/aiogramui | pypi: https://pypi.org/project/aiogramui
# -------------------------------------
# element Checkbox

from aiogram.types import CallbackQuery

class Checkbox:
    def __init__(self, off: str, on: str, keyboard, default: bool = False, chats: dict[int, bool] = {}, filters=[]):
        self.off, self.on = off, on
        self.keyboard = keyboard
        self.default = default
        self.chats = chats
        self.filters = filters
    
    def __call__(self, func):
        self.func = func

        return func
    
    def _check(self, chat):
        if chat not in self.chats:
            self.chats[chat] = self.default
    
    async def switch(self, cq: CallbackQuery):
        chat = cq.message.chat.id

        self._check(chat)  
        self.chats[chat] = not self.chats[chat]

        await cq.message.edit_reply_markup(reply_markup=self.keyboard(cq).as_markup())

        await self.func(cq.message, self.chats[chat])
    
    def text(self, chat: int) -> str:
        self._check(chat)

        return self.on if self.chats[chat] else self.off