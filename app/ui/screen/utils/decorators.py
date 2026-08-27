from functools import wraps


def lazy_create(attr_name: str):
    '''
    Checks for the existence of the created field before attempting to create it.
    If the field is found, ignores the execution of the create function.

    :param attr_name: is primary_key value for identify fields.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, attr_name):
                return
            return func(self, *args, **kwargs)
        return wrapper
    return decorator