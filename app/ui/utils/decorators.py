from functools import wraps


def lazy_create(attr_name: str):

    def decorator(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, attr_name):
                return

            return func(self, *args, **kwargs)

        return wrapper
    return decorator
