# main.py | part of aiogramui framework
# author: evryoneowo | year: 2025
# github: https://github.com/evryoneowo/aiogramui | pypi: https://pypi.org/project/aiogramui
# -------------------------------------
# frontend of aiogramui | connects elements

from logging import getLogger

from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .dialog import Dialog
from .button import Button
from .checkbox import Checkbox
from .custom import Custom

logger = getLogger('aiogramui')

router = None
def init(r: Router):
    '''Initialaze your aiogram.Router'''

    global router

    router = r

class Root:
    '''Class of page.'''

    cqs = []

    def __init__(self, text: str, backtext: str, back=False, filters=[]):
        '''Initialaze root page.'''

        self.text = text
        self.backtext = backtext
        self.back = back
        self.filters = filters

        self.local = []
        if not back:
            Root.cqs.append(self)
    
    def page(self, text: str, *filters):
        '''Add child page.'''
        
        root = Root(text, self.backtext, back=self, filters=filters)

        Root.cqs.append(root)
        self.local.append(root)

        return root
    
    def dialog(self, text: str, *filters) -> Dialog:
        '''Add dialog to page.'''

        dialog = Dialog(text, self, router, filters=filters)

        Root.cqs.append(dialog)
        self.local.append(dialog)

        return dialog
    
    def button(self, text: str, *filters) -> Button:
        '''Add button to page.'''

        button = Button(text, filters=filters)

        Root.cqs.append(button)
        self.local.append(button)

        return button
    
    def checkbox(self, off: str, on: str, *filters, default: bool = False, chats: dict[int, bool] = {}) -> Checkbox:
        '''Add checkbox to page.'''

        checkbox = Checkbox(off, on, self.keyboard, default, chats, filters=filters)

        Root.cqs.append(checkbox)
        self.local.append(checkbox)

        return checkbox

    def keyboard(self, data: Message | CallbackQuery, adjust: int = 2) -> InlineKeyboardBuilder:
        '''Get an aiogram.utils.keyboard.InlineKeyboardBuilder of current page.'''

        k = InlineKeyboardBuilder()

        for i in self.local:
            if isinstance(i, Root) and not all(map(lambda x: x(data), i.filters)):
                continue
            
            if isinstance(i, Checkbox):
                if isinstance(data, Message):
                    chat = data.chat.id
                else:
                    chat = data.message.chat.id

                k.button(
                    text=i.text(chat),
                    callback_data=str(Root.cqs.index(i))
                )
            else:
                k.button(
                    text=i.text,
                    callback_data=str(Root.cqs.index(i))
                )
        
        if self.back:
            k.button(
                text=self.backtext,
                callback_data=str(Root.cqs.index(self.back))
            )

        k.adjust(adjust)
        
        return k
    
    def generate_doc(self) -> str:
        '''Generate doc.'''

        txt = f'{self.text} - {self.func.__doc__}' if self.func.__doc__ else self.text
        for i in self.local:
            if not isinstance(i, Root):
                txt += f'\n    {i.text}'
            else:
                if i.allow:
                    continue
                for j in i.generate_doc().split('\n'):
                    txt += f'\n    {j}'
        
        return txt
    
    def __call__(self, func):
        self.func = func

        return func

handlers = {}
def handle(cqdata, *filters) -> Custom:
    '''Handle custom callback query. You can use "data", e.g. "len(data) == 5".'''

    global handlers

    custom = Custom(filters)
    handlers[cqdata] = custom

    return custom

def register():
    '''Register all Callback Queries.'''

    async def handler(cq: CallbackQuery):
        try:
            data = int(cq.data)
        except:
            data = cq.data

            if data in handlers:
                if all(map(lambda x: x(cq), handlers[data].filters)) or not handlers[data].filters :
                    await handlers[data].func(cq)
            else:
                for cqdata in handlers:
                    if not isinstance(cqdata, str):
                        if cqdata(data) and all(map(lambda x: x(cq), handlers[cqdata].filters)) or not handlers[cqdata].filters:
                            await handlers[cqdata].func(cq)

            logging.info(f'{cq.from_user.id} clicked "{data}" custom button')
            return

        element = Root.cqs[data]

        if not all(map(lambda x: x(cq), element.filters)) and element.filters:
            return

        msg = cq.message

        tp = type(element)

        if tp == Dialog:
            await msg.delete()
            await element.start(msg)
            logging.info(f'{cq.from_user.id} started "{element.name}" dialog')
        elif tp == Button:
            await element.func(cq)
            logging.info(f'{cq.from_user.id} clicked "{element.name}" button')
        elif tp == Checkbox:
            await element.switch(cq)
            logging.info(f'{cq.from_user.id} clicked "{element.name}" checkbox')
        elif tp == Root:
            await msg.delete()
            await element.func(msg, element.keyboard(cq))
            logging.info(f'{cq.from_user.id} entered "{element.name}" page')

    router.callback_query.register(handler)
