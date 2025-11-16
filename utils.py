#!/usr/bin/env python3
"""Utility functions."""

import requests
from functools import wraps
from typing import Mapping, Sequence, Any, Callable


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested map using a sequence of keys."""
    current = nested_map
    for key in path:
        current = current[key]
    return current


def get_json(url: str) -> Mapping:
    """Get JSON payload from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> property:
    """Decorator to memoize method results."""
    attr_name = "_memoized_" + fn.__name__

    @property
    @wraps(fn)
    def memoizer(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoizer
