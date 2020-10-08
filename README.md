# one-line_methods
Run methods in one line even if they do not return 'self'.

Say, we have:

    a = {1: 'x', 2: 'y'}
    b = {2: 'z', 3: 'y'}


You can't do this to merge them because 'update' returns None and not self:

    c = a.copy().update(b)
    # c = None

Using 'take' with dicts*:

    c = take(a.copy()).update(b).update({42: 'k'}).unwrap()

    # c = {1: 'x', 2: 'z', 3: 'y', 42: 'k'}
    # a = {1: 'x', 2: 'y'}
    # b = {2: 'z', 3: 'y'}

    *Dicts are taken for the purpose of example. There are obviously better ways to merge dicts.

With lists:

    c = take([1, 2, 3]).append(4).extend([5, 6]).unwrap()
    # c = [1, 2, 3, 4, 5, 6]


Without assigning:

    a = {}
    take(a).update({1: 'x', 2: 'y'}).update({3: 'z'})
    # a = {1: 'x', 2: 'y', 3: 'z'}
    
    b = [1, 2]
    take(b).append(3).extend([4, 5])
    # b = [1, 2, 3, 4, 5]
