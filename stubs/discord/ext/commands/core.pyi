from typing import Any, Callable, Dict, Optional, Iterator, Union, Awaitable, Type, ValuesView, List, TypeVar
from .context import Context
from .cooldowns import CooldownMapping, BucketType

CallbackType = Callable[..., Awaitable[Any]]
ErrorHandlerType = Callable[..., Awaitable[None]]
CheckType = Union[Callable[[Context], bool],
                  Callable[[Context], Awaitable[bool]]]


class Command:
    name: str
    callback: CallbackType
    help: str
    brief: str
    usage: str
    aliases: List[str]
    enabled: bool
    parent: Optional['Command']
    checks: List[CheckType]
    description: str
    hidden: bool
    _buckets: CooldownMapping

    def __init__(self, name: str, callback: CallbackType, *, enabled: bool = ...,
                 help: Optional[str] = ..., brief: Optional[str] = ..., usage: Optional[str] = ...,
                 rest_is_raw: bool = ..., aliases: List[str] = ..., description: str = ...,
                 hidden: bool = ...) -> None: ...

    def error(self, coro: ErrorHandlerType) -> ErrorHandlerType: ...

    @property
    def qualified_name(self) -> str: ...

    @property
    def cog_name(self) -> Optional[str]: ...

    @property
    def short_doc(self) -> str: ...

    def is_on_cooldown(self, ctx: Context) -> bool: ...

    def reset_cooldown(self, ctx: Context) -> None: ...

    async def do_conversion(self, ctx: Context, converter: Any, argument: str) -> Any: ...


class GroupMixin:
    all_commands: Dict[str, Command]
    case_insensitive: bool

    @property
    def commands(self) -> ValuesView[Command]: ...

    def recursively_remove_all_commands(self) -> None: ...

    def add_command(self, command: Command) -> None: ...

    def remove_command(self, name: str) -> Optional[Command]: ...

    def walk_commands(self) -> Iterator[Command]: ...

    def get_command(self, name: str) -> Optional[Command]: ...

    def command(self, *args, **kwargs) -> Callable[[CallbackType], Command]: ...

    def group(self, *args, **kwargs) -> Callable[..., Command]: ...


class Group(GroupMixin, Command):
    invoke_without_command: bool


FuncType = Callable[..., Any]
F = TypeVar('F', bound=Union[FuncType, Command])


def command(name: Optional[str] = ..., cls: Optional[Type[Command]] = ..., **kwargs) -> Callable[..., Command]: ...


def group(name: Optional[str] = ..., cls: Optional[Type[Group]] = ..., **kwargs) -> Callable[..., Group]: ...


def check(predicate: CheckType) -> Callable[[F], F]: ...


def has_role(name: str) -> Callable[[F], F]: ...


def has_any_role(*names: str) -> Callable[[F], F]: ...


def has_permissions(**perms: bool) -> Callable[[F], F]: ...


def bot_has_role(*names: str) -> Callable[[F], F]: ...


def bot_has_permissions(**perms: bool) -> Callable[[F], F]: ...


def guild_only() -> Callable[[F], F]: ...


def is_owner() -> Callable[[F], F]: ...


def is_nsfw() -> Callable[[F], F]: ...


def cooldown(rate: int, per: float, type: BucketType = ...) -> Callable[[F], F]: ...
