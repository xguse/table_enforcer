"""Provide decoration functions to augment the behavior of validator functions."""
import functools

import pandas as pd
import numpy as np


def minmax(low, high):
    """Test whether series items are not less than/greater than lo/hi."""
    def decorator(function):
        """Decorate a function with args."""
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            """Wrap the function."""
            series = function(*args, **kwargs)
            lo_pass = low <= series
            hi_pass = series <= high

            return lo_pass & hi_pass

        return wrapper

    return decorator


