from aiogram.types import Message

class Checkbox:
    def __init__(self, off, on, keyboard, default=False, users={}, filters=[]):
        self.off, self.on = off, on
        self.keyboard = keyboard
        self.default = default
        self.users = users
        self.filters = filters
    
    def __call__(self, func):
        self.func = func

        return func
    
    def _check(self, user):
        if user not in self.users:
            self.users[user] = self.default

            return False
        else:
            return True
    
    async def switch(self, msg: Message, data):
        user = data.from_user.id

        self._check(user)  
        self.users[user] = not self.users[user]

        await msg.edit_reply_markup(reply_markup=self.keyboard(data).as_markup())

        await self.func(msg, self.users[user])
    
    def text(self, user):
        self._check(user)

        return self.on if self.users[user] else self.off