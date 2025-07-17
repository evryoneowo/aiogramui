class Custom:
    def __init__(self, filters=[]):
        self.filters = filters

    def __call__(self, func):
        self.func = func

        return func

class Text:
    def __str__(self):
        return lambda s: str(s)

    def __len__(self):
        return lambda s: len(s)

    def __contains__(self, item):
        return lambda s: item in s

    def __eq__(self, other):
        return lambda s: s == other

    def __add__(self, other):
        return lambda s: s + other

    def __getitem__(self, key):
        return lambda s: s[key]

    def upper(self):
        return lambda s: s.upper()

    def lower(self):
        return lambda s: s.lower()

    def split(self, sep=None):
        return lambda s: s.split(sep)

    def replace(self, old, new, count=-1):
        return lambda s: s.replace(old, new, count)

    def strip(self, chars=None):
        return lambda s: s.strip(chars)

    def find(self, sub, start=None, end=None):
        return lambda s: s.find(sub, start, end)

    def count(self, sub, start=None, end=None):
        return lambda s: s.count(sub, start, end)

    def format(self, *args, **kwargs):
        return lambda s: s.format(*args, **kwargs)

    def join(self, iterable):
        return lambda s: s.join(iterable)

    def startswith(self, prefix, start=None, end=None):
        return lambda s: s.startswith(prefix, start, end)

    def endswith(self, suffix, start=None, end=None):
        return lambda s: s.endswith(suffix, start, end)

data = Text()