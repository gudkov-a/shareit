# -*- coding: utf-8 -*-

from sys import argv


def skip_in_test(func):
    def wrapper(*args, **kwargs):
        if 'test' in argv:
            result = None
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper
