[![PyPI Package](https://img.shields.io/badge/package-aiogramui-blue)](https://pypi.org/project/aiogramui/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# aiogramui 1.1.2
✨ A minimalistic UI framework for aiogram bots.
Devlog - https://t.me/aiogramui/

## Installation
```bash
pip install aiogramui
```

## Documentation
### Pages
Let's create start page and child page "Wallet":
```python
from aiogramui import *

init(router)

startpage = Root('start', backtext='Back')
wallet = startpage.page('Wallet')

@startpage
@router.message(Command('start'))
async def on_start(msg: Message, keyboard=None):
    await msg.answer('start page', reply_markup=startpage.keyboard(msg).as_markup())

@wallet
async def on_wallet(msg: Message, keyboard=None):
    await msg.answer('wallet page', reply_markup=keyboard.as_markup())

register()
```

`init()` and `register()` are required. `Root()` - a root page that doesn't have back button. All pages has elements functions, to learn more about them, keep read.
### Elements
#### Dialog
```python
Root.dialog(text, *filters)
```
Usage:
```python
users = {
    'evr4': '1234',
    'evryoneowo': '1337',
    'bestusr': '111111'
}

login = start.dialog('Log in')

@passwd.arg('Enter your login')
async def on_login(msg: Message, args):
    login = args[0]
    if login not in users: return # If user entered not valid login then it will ask him again.

@passwd.arg('Enter the password')
async def on_passwd(msg: Message, args):
    password = users[args[0]]
    entered_password = args[1]
    if password != entered_password: await login.cancel(msg) # If user entered not valid password then it will cancel dialog.

    await msg.answer(f'Welcome, {args[0]}!')
```
#### Button
```python
Root.button(text, *filters)
```
Usage:
```python
hwbtn = start.button('Click me')

@hwbtn
async def on_hwbtn(msg: Message):
    await msg.answer('Hello, World!')
```
#### Checkbox
```python
Root.checkbox(off, on, *filters, default=False)
```
Usage:
```python
checkbox = start.checkbox('off', 'on')

@checkbox
async def on_checkbox(msg: Message, state):
    await msg.answer(f'State: {state}')
```
You can also save values of checkboxes for loading them later using `users` arg in `checkbox()`.
#### Handle
```python
handle(cqdata, *filters)
```
Usage:
If you has inline keyboard with cqdata "delete" that deletes message:
```python
@handle(data == 'hi')
async def on_hi(cq: CallbackQuery):
    await cq.message.delete()
```
### Filters
You can use filters at pages or elements. e. g.
```python
from aiogramui.filters import UserFilter

admins = [12453, 21546, 69283]

adminpage = start.page('Admin', UserFilter(admin))

@adminpage
async def on_adminpage(msg: Message, keyboard):
    await msg.answer('Admin page', reply_markup=keyboard.as_markup())
```
### Doc
```python
doc = start.generate_doc()
```

It will generate docs of your menu using docstrings for descriptions.