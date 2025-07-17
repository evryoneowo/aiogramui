class Button:
    def __init__(self, text, filters=[]):
        self.text = text
        self.filters = filters
    
    def __call__(self, func):
        self.func = func