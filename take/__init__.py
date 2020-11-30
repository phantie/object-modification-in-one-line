from functools import partial

__all__ = ('take',)

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
    
    def _dispatch_(self, taken):
        _ = taken
        for attrname in self.names:
            _ = getattr(_, attrname)

        if self.call_attrs is not None:
            call_args, call_kwargs = self.call_attrs
            _ = _(*call_args, **call_kwargs)

        return _

class self:
    def __getattr__(self, name):
        return selfattr(name)

take_self = self()

class Parent:

    def __init__(self, args, kwargs, taken, exec = True):
        self.args = args
        self.kwargs = kwargs
        self.taken = taken
        self.exec = exec

    def handle(self):
        taken = self.taken
        if not self.exec:
            args, kwargs = [], {}

        for arg in self.args:
            arg = self.handle_arg(arg)
            if self.exec:
                arg()
            else:
                args.append(arg)

        if not self.exec:
            return args, kwargs


    def handle_arg(self, _, outer=True):
        inst = partial(isinstance, _)
        
        if inst(tuple):
            return self.handle_arg(partial(*_), True)
        elif inst(partial):
            f = _.func
            args = _.args
            kwargs = _.keywords
            args = tuple(self.handle_arg(a, False) for a in args)
            kwargs = {k: self.handle_arg(v, False) for k, v in kwargs.items()}

            if args == _.args and kwargs == _.keywords:
                return partial(f, self.taken, *args, **kwargs)
            else:
                return partial(f, *args, **kwargs)
        elif inst(selfattr):
            dispatched = self.taken
            for attrname in _.names:
                dispatched = getattr(dispatched, attrname)

            if _.call_attrs is not None:
                args, kwargs = _.call_attrs

                args = tuple(self.handle_arg(a, False) for a in args)

                kwargs = {k: self.handle_arg(v, False) for k, v in kwargs.items()}

                if outer and self.exec:
                    return partial(dispatched, *args, **kwargs)
                elif outer and not self.exec:
                    return dispatched(*args, **kwargs)
                else:
                    return dispatched(*args, **kwargs)
            return dispatched
        elif _ is take_self:
            return self.taken

        else:
            if self.exec:
                if outer:
                    return partial(_, self.taken)
                else:
                    return _
            else:
                return _
            


class take:
    __slots__ = ('obj',)

    class mockmeth:
        def __init__(self, name, taken):
            self.name = name
            self.bounded = getattr(taken.obj, name)
            self.taken = taken

        def __call__(self, *args, **kwargs):
            args, kwargs = Parent(args, kwargs, self.taken.obj, False).handle()
            self.bounded(*args, **kwargs)
            return self.taken

    self = take_self

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        return self.mockmeth(name, self)

    def __call__(self, *args, **names_values):
        obj = self.obj

        Parent(args, {}, obj).handle()

        for k, v in names_values.items():
            setattr(obj, k, v)

        return self

    def unwrap(self):
        return self.obj