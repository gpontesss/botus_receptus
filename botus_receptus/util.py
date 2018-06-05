from typing import TypeVar, Iterable, Optional, Callable, Any, Iterator, Set, Container
from itertools import filterfalse

import discord

_T = TypeVar('_T')


def unique_seen(iterable: Iterable[_T], get_key: Optional[Callable[[_T], Any]] = None) -> Iterator[_T]:
    seen: Set[Any] = set()
    if get_key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen.add(element)
            yield element
    else:
        for element in iterable:
            key = get_key(element)
            if key not in seen:
                seen.add(key)
                yield element


def has_any_role(member: discord.Member, roles: Container[str]) -> bool:
    return discord.utils.find(lambda role: role.name in roles, member.roles) is not None


def has_any_role_id(member: discord.Member, ids: Container[int]) -> bool:
    return discord.utils.find(lambda role: role.id in ids, member.roles) is not None
