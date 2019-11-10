class Registable:
    @classmethod
    def get(cls, argument):
        if not hasattr(cls, 'REGISTERED'):
            setattr(cls, 'REGISTERED', dict())
        registered = cls.REGISTERED
        value = registered.get(argument, None)
        if value is None:
            registered[argument] = value = cls.make(argument)
        return value

    @classmethod
    def length(cls):
        if not hasattr(cls, 'REGISTERED'):
            return 0
        return len(cls.REGISTERED)