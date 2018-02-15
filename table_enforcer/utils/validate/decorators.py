"""Provide decoration functions to augment the behavior of validator functions."""
import functools


def minmax(low, high):
    """Test that the data items fall within range: low <= x <= high."""
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


def choice(choices):
    """Test that the data items are members of the set `choices`."""
    def decorator(function):
        """Decorate a function with args."""
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            """Wrap the function."""
            series = function(*args, **kwargs)
            return series.isin(set(choices))

        return wrapper

    return decorator


def bounded_length(low, high=None):
    """Test that the length of the data items fall within range: low <= x <= high.

    If high is None, treat as exact length.
    """
    def decorator(function):
        """Decorate a function with args."""
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            """Wrap the function."""
            series = function(*args, **kwargs)
            if high is None:
                return series.apply(lambda x: len(x) == low)
            else:
                lo_pass = series.apply(lambda x: low <= len(x))
                hi_pass = series.apply(lambda x: len(x) <= high)

                return lo_pass & hi_pass

        return wrapper

    return decorator

