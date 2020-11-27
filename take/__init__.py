class take:
    __slots__ = ('obj',)

    class mockmeth:
        def __init__(self, name, taken):
            self.name = name
            self.bounded = getattr(taken.obj, name)
            self.taken = taken

        def __call__(self, *args, **kwargs):
            self.bounded(*args, **kwargs)
            return self.taken

    @classmethod
    def _handle_partial(cls, f, taken):
        def replace_with(taken, args, kwargs):
            itself = cls.self
            selfattr = cls.selfattr

            args = tuple((taken if v is itself else v.dispatch(taken) if isinstance(v, selfattr) else v) for v in args)
            kwargs = {k: (taken if v is itself else v.dispatch(taken) if isinstance(v, selfattr) else v) for k, v in kwargs.items()}
            return args, kwargs

        from functools import partial

        if isinstance(f, take.selfattr):
            if f.call_attrs is None:
                raise TypeError(str(f.dispatch(taken)) + ' must be called/not be in this block')

            f.call_attrs = replace_with(taken, *f.call_attrs)
            f = partial(lambda _: _, f)

        altered = False
        if isinstance(f, partial):

            args, kwargs = replace_with(taken, f.args, f.keywords)
            altered = args != f.args or kwargs != f.keywords
            f = partial(f.func, *args, **kwargs)
        
        return f, altered

    class selfattr:
        def __init__(self, name):
            self.names = [name]
            self.call_attrs = None

        def __getattr__(self, name):
            self.names.append(name)
            self.call_attrs = None
            return self

        def __call__(self, *args, **kwargs):
            self.call_attrs = (args, kwargs)
            return self
        
        def dispatch(self, taken):
            _ = taken
            for attrname in self.names:
                _ = getattr(_, attrname)

            if self.call_attrs is not None:
                call_args, call_kwargs = self.call_attrs
                _ = _(*call_args, **call_kwargs)

            return _

    class self:
        def __getattr__(self, name):
            return take.selfattr(name)

    self = self()

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        return self.mockmeth(name, self)

    def __call__(self, *funcs, **names_values):
        obj = self.obj

        for f in funcs:
            f, altered = self._handle_partial(f, obj)
            f() if altered else f(obj)

        for k, v in names_values.items():
            setattr(obj, k, v)
        return self

    def unwrap(self):
        return self.obj

# from functools import partial
# def assert_eq(v1, v2):
#     def _assert_eq(v1, v2):
#         assert v1 == v2
#     return partial(_assert_eq, v1, v2)
    
