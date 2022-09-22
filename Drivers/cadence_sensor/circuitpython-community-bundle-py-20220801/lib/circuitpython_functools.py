# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT
"""
`circuitpython_functools`
================================================================================

A CircuitPython implementation of CPython's functools library.  Note that
this implementation is not a 1-to-1 replica, but rather provides the same
functionality with minor differences in usage.


* Author(s): Alec Delaney

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import gc

__version__ = "0.1.0"
__repo__ = "https://github.com/tekktrik/CircuitPython_functools.git"

cache_record = []

# pylint: disable=too-few-public-methods
class _ObjectMark:
    pass


def _make_key(args, kwargs, kwd_mark=(_ObjectMark(),)):
    key = tuple(args)
    if kwargs:
        key += kwd_mark
        for item in kwargs.items():
            key += tuple(item)
    return hash(key)


def cache(user_function):
    """Unbounded cache"""
    sentinel = object()
    cache_dict = {}
    cache_get = cache_dict.get

    def cache_wrapper(*args, **kwargs):
        key = _make_key(args, kwargs)
        result = cache_get(key, sentinel)
        if result is not sentinel:
            return result
        result = user_function(*args, **kwargs)
        cache_dict[key] = result
        return result

    cache_record.append(cache_dict)

    return cache_wrapper


def clear_caches():
    """Clears all the caches"""
    for cache_contents in cache_record:
        cache_contents.clear()
    gc.collect()


# Ported from the MicroPython library
def partial(func, *args, **kwargs):
    """Creates a partial of the function"""

    def _partial(*more_args, **more_kwargs):
        local_kwargs = kwargs.copy()
        local_kwargs.update(more_kwargs)
        return func(*(args + more_args), **local_kwargs)

    return _partial
