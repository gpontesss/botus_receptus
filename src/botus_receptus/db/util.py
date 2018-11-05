from __future__ import annotations

from typing import Sequence, List, Any, Optional, Tuple, Dict
from asyncpg import Connection

__all__ = ('select_all', 'select_one', 'insert_into', 'delete_from', 'search')


def _get_join_string(joins: Optional[Sequence[Tuple[str, str]]]) -> str:
    if joins is None or len(joins) == 0:
        return ''

    return ' ' + ' '.join(map(lambda join: f'JOIN {join[0]} ON {join[1]}', joins))


def _get_where_string(conditions: Optional[Sequence[str]]) -> str:
    if conditions is None or len(conditions) == 0:
        return ''

    return ' WHERE ' + ' AND '.join(conditions)


def _get_order_by_string(order_by: Optional[str]) -> str:
    if order_by is None:
        return ''

    return f' ORDER BY {order_by} ASC'


def _get_group_by_string(group_by: Optional[Sequence[str]]) -> str:
    if group_by is None:
        return ''

    return ' GROUP BY ' + ', '.join(group_by)


async def select_all(db: Connection, *args: Any,
                     table: str,
                     columns: Sequence[str],
                     where: Optional[Sequence[str]] = None,
                     group_by: Optional[Sequence[str]] = None,
                     order_by: Optional[str] = None,
                     joins: Optional[Sequence[Tuple[str, str]]] = None) -> List[Any]:
    columns_str = ', '.join(columns)
    where_str = _get_where_string(where)
    joins_str = _get_join_string(joins)
    group_by_str = _get_group_by_string(group_by)
    order_by_str = _get_order_by_string(order_by)

    return await db.fetch(
        f'SELECT {columns_str} FROM {table}{joins_str}{where_str}{group_by_str}{order_by_str}',
        *args
    )


async def select_one(db: Connection, *args: Any,
                     table: str,
                     columns: Sequence[str],
                     where: Optional[Sequence[str]] = None,
                     group_by: Optional[Sequence[str]] = None,
                     joins: Optional[Sequence[Tuple[str, str]]] = None) -> Optional[Any]:
    columns_str = ', '.join(columns)
    where_str = _get_where_string(where)
    joins_str = _get_join_string(joins)
    group_by_str = _get_group_by_string(group_by)

    return await db.fetchrow(
        f'SELECT {columns_str} FROM {table}{joins_str}{where_str}{group_by_str}',
        *args
    )


async def search(db: Connection, *args: Any,
                 table: str,
                 columns: Sequence[str],
                 search_columns: Sequence[str],
                 terms: Sequence[str],
                 where: Sequence[str] = [],
                 group_by: Optional[Sequence[str]] = None,
                 order_by: Optional[str] = None,
                 joins: Optional[Sequence[Tuple[str, str]]] = None) -> List[Any]:
    columns_str = ', '.join(columns)
    joins_str = _get_join_string(joins)
    search_columns_str = " || ' ' || ".join(search_columns)
    search_terms_str = ' & '.join(terms)
    where_str = _get_where_string(tuple(where) + (
        f"to_tsvector('english', {search_columns_str}) @@ to_tsquery('english', '{search_terms_str}')",
    ))
    group_by_str = _get_group_by_string(group_by)
    order_by_str = _get_order_by_string(order_by)

    return await db.fetch(
        f'SELECT {columns_str} FROM {table}{joins_str}{where_str}{group_by_str}{order_by_str}',
        *args
    )


async def update(db: Connection, *args: Any,
                 table: str,
                 values: Dict[str, Any],
                 where: Sequence[str] = []) -> None:
    set_str = ', '.join([' = '.join([key, value]) for key, value in values.items()])
    where_str = _get_where_string(where)

    await db.execute(f'UPDATE {table} SET {set_str}{where_str}', *args)


async def insert_into(db: Connection, *, table: str,
                      values: Dict[str, Any],
                      extra: str = '') -> None:
    columns: List[str] = []
    data: List[Any] = []

    for column, value in values.items():
        columns.append(column)
        data.append(value)

    if extra:
        extra = ' ' + extra

    columns_str = ', '.join(columns)
    values_str = ', '.join(map(lambda index: f'${index}', range(1, len(values) + 1)))
    await db.execute(f'INSERT INTO {table} ({columns_str}) VALUES ({values_str}){extra}', *data)


async def delete_from(db: Connection, *args: Any, table: str, where: Sequence[str]) -> None:
    where_str = _get_where_string(where)
    await db.execute(f'DELETE FROM {table}{where_str}', *args)