# Stubs for asyncpg.pool (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from . import connection
from .protocol import Record
from typing import Any, Optional, Type, Callable, Iterable, Sequence, List, AsyncContextManager, Awaitable, Generator
from asyncio import AbstractEventLoop
from .connection import Connection

class PoolConnectionProxyMeta(type):
    def __new__(mcls: Any, name: Any, bases: Any, dct: Any, *, wrap: bool = ...): ...
    def __init__(cls, name: Any, bases: Any, dct: Any, *, wrap: bool = ...) -> None: ...

class PoolConnectionProxy(connection._ConnectionProxy):
    def __init__(self, holder: 'PoolConnectionHolder', con: Connection) -> None: ...
    def __getattr__(self, attr): ...

class PoolConnectionHolder:
    def __init__(self, pool: Any, max_queries: Any, setup: Any, max_inactive_time: Any) -> None: ...
    async def connect(self) -> None: ...
    async def acquire(self) -> PoolConnectionProxy: ...
    async def release(self, timeout: float): ...
    async def wait_until_released(self): ...
    async def close(self) -> None: ...
    def terminate(self) -> None: ...

class Pool(AsyncContextManager['Pool'], Awaitable['Pool']):
    def __init__(self, *connect_args, min_size, max_size, max_queries, max_inactive_connection_lifetime, setup, init, loop, connection_class, **connect_kwargs) -> None: ...
    def _async__init__(self): ...
    def set_connect_args(self, dsn: Optional[str] = ..., **connect_kwargs: Any) -> None: ...
    async def execute(self, query: str, *args: Any, timeout: float = ...) -> str: ...
    async def executemany(self, command: str, args: Iterable[Sequence[Any]], *, timeout: float = ...) -> None: ...
    async def fetch(self, query: str, *args: Any, timeout: float = ...) -> List[Record[Any]]: ...
    async def fetchval(self, query: str, *args: Any, column: int = ..., timeout: float = ...) -> Optional[Any]: ...
    async def fetchrow(self, query: str, *args: Any, timeout: float = ...) -> Optional[Record[Any]]: ...
    def acquire(self, *, timeout: Optional[float] = ...) -> 'PoolAcquireContext': ...
    async def release(self, connection: Connection) -> None: ...
    async def close(self) -> None: ...
    def terminate(self) -> None: ...
    async def expire_connections(self) -> None: ...
    def __await__(self) -> Generator[Any, None, 'Pool']: ...
    async def __aenter__(self): ...
    async def __aexit__(self, *exc: Any) -> None: ...

class PoolAcquireContext(AsyncContextManager[Connection], Awaitable[Connection]):
    pool: Any = ...
    timeout: Any = ...
    connection: Any = ...
    done: bool = ...
    def __init__(self, pool, timeout) -> None: ...
    async def __aenter__(self) -> Connection: ...
    async def __aexit__(self, *exc: Any) -> None: ...
    def __await__(self) -> Generator[Any, None, Connection]: ...

def create_pool(dsn: Optional[str] = ..., *, min_size: int = ..., max_size: int = ..., max_queries: int = ...,
                max_inactive_connection_lifetime: float = ...,
                setup: Optional[Callable[[PoolConnectionProxy], Any]] = ...,
                init: Optional[Callable[[Connection], Any]] = ...,
                loop: Optional[AbstractEventLoop] = ..., connection_class: Type[Connection] = ...,
                **connect_kwargs: Any) -> Pool: ...