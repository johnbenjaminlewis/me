class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


def deep_merge(base, updates):
    """ apply updates to base dictionary
    """
    for key, value in updates.iteritems():
        if key in base and isinstance(value, dict):
            base[key] = deep_merge(base[key] or {}, value)
        else:
            base[key] = value
    return base
