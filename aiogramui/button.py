# button.py | part of aiogramui framework
# author: evryoneowo | year: 2025
# github: https://github.com/evryoneowo/aiogramui | pypi: https://pypi.org/project/aiogramui
# -------------------------------------
# element Button

class Button:
    def __init__(self, text, filters=[]):
        self.text = text
        self.filters = filters
    
    def __call__(self, func):
        self.func = func