"""
Test module A for gousset testing.
Contains functions with nested calls and different timing characteristics.
"""

import time


def fast_function():
    """A fast function for testing"""
    time.sleep(0.001)
    return "fast result"


def slow_function():
    """A slower function that calls fast_function internally"""
    time.sleep(0.005)
    fast_function()  # This creates a nested call
    return "slow result"


def medium_function():
    """A medium-speed function"""
    time.sleep(0.003)
    return "medium result"