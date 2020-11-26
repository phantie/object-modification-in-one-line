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
    def handle_partial(cls, f, taken):
        from functools import partial
        altered = False
        if isinstance(f, partial):
            args, kwargs = cls.self.replace_with(taken, f.args, f.keywords)
            altered = args != f.args or kwargs != f.keywords
            f = partial(f.func, *args, **kwargs)

        return f, altered


    class self:
        @classmethod
        def replace_with(cls, taken, args, kwargs):
            idx = args.index(cls)
            args = list(args)
            args[idx] = taken
            kwargs = {k: (taken if v is cls else v) for k, v in kwargs.items()}
            return tuple(args), kwargs

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        return self.mockmeth(name, self)

    def __call__(self, *funcs, **names_values):
        obj = self.obj

        for f in funcs:
            f, altered = self.handle_partial(f, obj)
            f() if altered else f(obj)

        for k, v in names_values.items():
            setattr(obj, k, v)
        return self

    def unwrap(self):
        return self.obj