def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def singleton_creator(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instance = cls(*args, **kwargs)
            instances[cls] = instance.create()
        return instances[cls]
    return get_instance
