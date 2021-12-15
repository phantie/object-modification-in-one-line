# attribute setting and method calling in one line
Execute methods even if they do not return the object they are bound to, set attributes and execute functions over stored objects in one line.

### Overview:
    
    class A:
        secret = 8
        def __init__(self, some):
            self.some = some

        def reset(self):
            self.some = 0

    a = A(69)

Comparison:

    take(a)(secret=42, new=0).reset()(some=13)
   
VS
  
    a.secret, a.new = 42, 0
    a.reset()
    a.some = 13
  
We get the same result:

    assert a.secret == 42 and a.some == 13 and a.new == 0

But more concise and readable solution.

### Explanation:

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


Example with no assignment:

    a = {}
    take(a).update({1: 'x', 2: 'y'}).update({3: 'z'})
    # a = {1: 'x', 2: 'y', 3: 'z'}
    
    b = [1, 2]
    take(b).append(3).extend([4, 5])
    # b = [1, 2, 3, 4, 5]


If obj does not have a method you can do this:

    take([1,2,3])(print, partial(list.append, take.self, 4), print, list.clear, print)
    # stdout:
    [1, 2, 3]
    [1, 2, 3, 4]
    []

    # * usually you don't need an underlying object even using partial,
    # but list.append does NOT take keyword arguments, 
    # so it doesn't work: partial(list.append, object=4)

One more:


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


Install:

    pip install git+https://github.com/phantie/take.git

Use:

    from take import take
