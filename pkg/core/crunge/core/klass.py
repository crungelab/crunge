def producer(cls):
    def produce_instance(*args, **kwargs):
        instance = cls(*args, **kwargs)
        return instance.create()
    return produce_instance

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def singleton_producer(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instance = cls(*args, **kwargs)
            instances[cls] = instance.create()
        return instances[cls]
    return get_instance
