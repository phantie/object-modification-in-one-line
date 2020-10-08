class take:
    class mockmeth:
        def __init__(self, name, taken):
            self.name = name
            self.bounded = getattr(taken.obj, name)
            self.taken = taken

        def __call__(self, *args, **kwargs):
            self.bounded(*args, **kwargs)
            return self.taken

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        return self.mockmeth(name, self)

    def unwrap(self):
        return self.obj
