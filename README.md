# attribute setting and method calling in one line
Execute methods even if they do not return the object they are bound to and set attributes in one line.

Say, we have:

    a = {1: 'x', 2: 'y'}
    b = {2: 'z', 3: 'y'}


You can't do this to merge them because 'update' returns None and not self:

    c = a.copy().update(b)
    # c = None

Using 'take':

    c = take(a.copy()).update(b).update({42: 'k'}).unwrap()

    # c = {1: 'x', 2: 'z', 3: 'y', 42: 'k'}
    # a = {1: 'x', 2: 'y'}
    # b = {2: 'z', 3: 'y'}


Without assigning:

    a = {}
    take(a).update({1: 'x', 2: 'y'}).update({3: 'z'})
    # a = {1: 'x', 2: 'y', 3: 'z'}
    
    b = [1, 2]
    take(b).append(3).extend([4, 5])
    # b = [1, 2, 3, 4, 5]

Change attributes:
    
    class A:
        secret = 8
        def __init__(self, some):
            self.some = some

        def reset(self):
            self.some = 0

    a = A(69)
    take(a)(secret=42, new=0).reset()(some=13)
    assert a.secret == 42 and a.some == 13 and a.new == 0
