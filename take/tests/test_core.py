import pytest
from .. import take
from functools import partial

# def get_partial(f):
#     return f

# def assert_eq(v1, v2):
#     assert v1 == v2

# assert_eq = get_partial(assert_eq)

def assert_eq(v1, v2):
    def _assert_eq(v1, v2):
        assert v1 == v2
    return partial(_assert_eq, v1, v2)
    
def assert_ne(v1, v2):
    def _assert_ne(v1, v2):
        assert v1 != v2
    return partial(_assert_ne, v1, v2)

def test_case1():
    class A:
        secret = 8
        def __init__(self, some):
            self.some = some

        def reset(self):
            self.some = 0

    a = A(69)
    take(a)(secret=42, new=0).reset()(some=13)
    assert a.secret == 42 and a.new == 0 and a.some == 13

def test_case2():
    a = {1: 'x', 2: 'y'}
    b = {2: 'z', 3: 'y'}

    c = take(a.copy()).update(b).update({42: 'k'}).unwrap()

    assert c == {1: 'x', 2: 'z', 3: 'y', 42: 'k'}
    assert a == {1: 'x', 2: 'y'}
    assert b == {2: 'z', 3: 'y'}

def test_case3():
    a = {}
    take(a).update({1: 'x', 2: 'y'}).update({3: 'z'})
    assert a == {1: 'x', 2: 'y', 3: 'z'}

    b = [1, 2]
    take(b).append(3).extend([4, 5])
    assert b == [1, 2, 3, 4, 5]

def test_case4(capsys):
    take([1,2,3])(print, partial(list.append, take.self, 4), print, list.clear, print)

    assert capsys.readouterr().out == "[1, 2, 3]\n[1, 2, 3, 4]\n[]\n"

def test_case5(capsys):
    def sum_of(self, attr1, attr2):
        self.sum = attr1 + attr2

    class A:
        berries = 10
        carrots = 7
        peaches = 3

    a = A()
    take(a)(partial(sum_of, take.self, take.self.berries, take.self.carrots), partial(print, take.self.sum))

    assert capsys.readouterr().out == "17\n"
    assert a.sum == 17
    take(a)(partial(sum_of, take.self, take.self.carrots, take.self.peaches))
    assert a.sum == 10

def test_case6():
    class A: 
        v = 0
        def inc_v(self):
            self.v += 1
        def dec_v(self):
            self.v -= 1

    a = A()

    (take(a)(
        assert_eq(take.self.v, 0))
        .inc_v()
        .inc_v()(
            assert_eq(take.self.v, 2),
        )(v=10, x=0)
        .dec_v()(
            assert_eq(take.self.v, 9),
            assert_eq(take.self.x, 0),
        )
    )