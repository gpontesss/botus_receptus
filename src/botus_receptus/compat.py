from __future__ import annotations

import sys
from typing import Final

if sys.version_info >= (3, 9):
    from builtins import dict, list, tuple, type
    from collections.abc import (
        AsyncIterable,
        Awaitable,
        Callable,
        Container,
        Coroutine,
        Generator,
        Iterable,
        Iterator,
        Mapping,
        Sequence,
    )
    from contextlib import AbstractAsyncContextManager
    from re import Pattern
else:
    from typing import AsyncContextManager as AbstractAsyncContextManager
    from typing import AsyncIterable, Awaitable, Callable, Container, Coroutine
    from typing import Dict as dict
    from typing import Generator, Iterable, Iterator
    from typing import List as list
    from typing import Mapping, Pattern, Sequence
    from typing import Tuple as tuple
    from typing import Type as type

__all__: Final = (
    'AbstractAsyncContextManager',
    'AsyncIterable',
    'Awaitable',
    'Callable',
    'Container',
    'Coroutine',
    'Generator',
    'Iterable',
    'Iterator',
    'Mapping',
    'Pattern',
    'Sequence',
    'dict',
    'list',
    'tuple',
    'type',
)
