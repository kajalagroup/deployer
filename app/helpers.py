from datetime import time


def time_in_range(start: time, end: time, x: time):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
