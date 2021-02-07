"""In case of this particular project I write test also because I'm not sure how it works..."""

from .. import take
from ..tools import *

from functools import partial

import pytest


self = take.self

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
    take([1,2,3])(print, partial(list.append, self, 4), print, list.clear, print)

    assert capsys.readouterr().out == "[1, 2, 3]\n[1, 2, 3, 4]\n[]\n"

def test_case5(capsys):
    def sum_of(self, attr1, attr2):
        self.sum = attr1 + attr2

    class A:
        berries = 10
        carrots = 7
        peaches = 3

    a = A()
    take(a)(partial(sum_of, self, self.berries, self.carrots), partial(print, self.sum))

    assert capsys.readouterr().out == "17\n"
    assert a.sum == 17
    take(a)(partial(sum_of, self, self.carrots, self.peaches))
    assert a.sum == 10

def test_case6():
    class A: 
        x = 0
        def inc_x(self):
            self.x += 1
        def dec_x(self):
            self.x -= 1
        @classmethod
        def double_x(self):
            self.x *= 2

    a = A()

    (take(a)(
        assert_eq(self.x, 0))
        .inc_x()
        .inc_x()(
            assert_eq(self.x, 2),
        )(x=10, z=0)
        .dec_x()(
            assert_eq(self.x, 9),
            assert_eq(self.z, 0),
        )
    )
    take(A)(x=1)(
        self.double_x(),
        assert_eq(self.x, 2)
    )

def test_case7():
    class A:
        foo = 5
        class B:
            foo = 7

            @classmethod
            def double_foo(cls):
                cls.foo *= 2

            @classmethod
            def inc_foo_by(cls, value):
                cls.foo += value

            class C:
                foo = 9

    a = A()

    take(a)(
        assert_eq(self.foo, 5),
        assert_eq(self.B.foo, 7),
        self.B.double_foo(),
        assert_eq(self.B.foo, 14),
        self.B.inc_foo_by(self.foo),
        assert_eq(self.B.foo, 19),
        assert_eq(self.B.C.foo, 9),
    )

def test_case8():
    class A:
        foo = 10

        def get_value(self, value):
            return value * 3

        def add_to_foo(self, value):
            self.foo += value

    a = A()

    (take(a)
        (assert_eq(self.foo, 10), foo=20)
        (assert_eq(self.foo, 20), bar=40)
        (assert_eq(self.bar, 40))
        (partial(A.add_to_foo, self, self.get_value(5)))
        (assert_eq(self.foo, 35))
        )

def test_case9():
    def sum_of(self, attr1, attr2):
        self.sum = attr1 + attr2

    class A:
        berries = 10
        carrots = 7
        peaches = 3

    a = A()
    take(a)(
        (sum_of, self, self.berries, self.carrots), 
        (print, self.sum),
        assert_eq(self.sum, 17),
        (sum_of, self, self.carrots, self.peaches),
        assert_eq(self.sum, 10),
        )(sum = None)(
        assert_eq(self.sum, None)
        )

def test_case10():
    class A:
        def __init__(self, x):
            self.x=x
        def __eq__(self, other):
            return other.x == self.x
        def set_x(self, new):
            self.x = new

    take(A(10))(
        assert_eq_self(A(10))
    ).set_x(20)(
        assert_ne_self(A(10)),
        assert_eq_self(A(20))
    )

def test_case11():
    class A:
        foo = 5
        class B:
            foo = 7

            @classmethod
            def double_foo(cls):
                cls.foo *= 2

            @classmethod
            def inc_foo_by(cls, value):
                cls.foo += value

            class C:
                foo = 9

                @classmethod
                def get_hash(cls):
                    return cls.foo * 3

                @classmethod
                def get_strong_hash(cls, universe):
                    return cls.get_hash() + universe


    a = A()

    take(a)(
        self.B.inc_foo_by(self.B.C.get_hash()),
        assert_eq(self.B.foo, 7+27),
        self.B.inc_foo_by(self.B.C.get_strong_hash(6)),
        assert_eq(self.B.foo, 7+27+27+6),
        self.B.inc_foo_by(self.B.C.get_strong_hash(self.B.C.get_hash())),
        assert_eq(self.B.foo, 121),
    )

def test_case12():
    take([1, 2, 3]).extend(self)(assert_eq_self([1, 2, 3, 1, 2 ,3]))
    take([1, 2, 3]).append(self.index(3))(assert_eq_self([1, 2, 3, 2]))
    take([1, 2, 3]).extend(self).extend(self)(assert_eq_self([1, 2, 3] * 2 * 2))

def test_case13():
    class A:
        a = 0
        b = 1
        @classmethod
        def set_a_to_value(cls, value=None):
            cls.a = value

    (take(A)
        .set_a_to_value()
            (assert_eq(self.a, None))
        .set_a_to_value(self.b)
            (assert_eq(self.a, 1))
        .set_a_to_value(10)
            (assert_eq(self.a, 10))
        .set_a_to_value(value=self.b)
            (assert_eq(self.a, 1))
    )