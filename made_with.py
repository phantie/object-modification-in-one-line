
class General:
    def __init__(self, o, begin, end):
        self.o = o
        self.begin = begin 
        self.end = end

    def __enter__(self):
        return self.begin(self.o)
    
    def __exit__(self, type, value, tb):
        self.end(self.o)

from take import take

class B: ...

with General(
    B
    , lambda _: take(_)(__name__ = 'C').unwrap()
    , lambda _: take(_)(__name__ = 'B').unwrap()) as B:
    assert B.__name__ == 'C'

assert B.__name__ == 'B'
from functools import partial
class change_attr(General):
    def __init__(self, o, **name_value):
        self.o = o
        self.begin = lambda _: take(_)(**name_value).unwrap()

        old_name_value = {n: getattr(o, n) for n in name_value}
        self.end = lambda _: take(_)(**old_name_value)

def attrs(o):
    def wrap(**name_value):
        return change_attr(o, **name_value)
    return wrap

with attrs(B)(__name__ = 'C') as B:
    assert B.__name__ == 'C'

assert B.__name__ == 'B'