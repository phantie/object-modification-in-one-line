from functools import partial

def _assert_eq(v1, v2):
    assert v1 == v2

def _assert_ne(v1, v2):
    assert v1 != v2

def assert_eq_self(_):
    return partial(_assert_eq, v2=_)

def assert_ne_self(_):
    return partial(_assert_ne, v2=_)

def assert_eq(v1, v2):
    return partial(_assert_eq, v1, v2)
    
def assert_ne(v1, v2):
    return partial(_assert_ne, v1, v2)