from typing import Any, Optional

import discord
import pytest
from attr import dataclass
from discord.ext import typed_commands

from botus_receptus.db import Context

from ..types import Mocker


@dataclass(slots=True)
class MockBot(object):
    pool: Any


@dataclass(slots=True)
class MockUser(object):
    bot: Optional[bool] = None
    id: Optional[int] = None
    mention: Optional[str] = None


@dataclass(slots=True)
class MockMessage(object):
    author: Optional[MockUser] = None
    content: Optional[str] = None
    channel: Optional[discord.abc.GuildChannel] = None
    _state: Any = None


@dataclass(slots=True)
class MockCommand(object):
    ...


class TestContext(object):
    @pytest.fixture
    def mock_bot(self, mocker: Mocker) -> MockBot:
        class MockPool:
            acquire = mocker.CoroutineMock()
            release = mocker.CoroutineMock()

        return MockBot(pool=MockPool())

    @pytest.fixture
    def mock_mesage(self) -> MockMessage:
        return MockMessage()

    @pytest.fixture
    def mock_command(self) -> MockCommand:
        return MockCommand()

    @pytest.fixture
    def mock_select_all(self, mocker: Mocker) -> Any:
        return mocker.patch(
            'botus_receptus.db.context.select_all', new_callable=mocker.CoroutineMock
        )

    @pytest.fixture
    def mock_select_one(self, mocker: Mocker) -> Any:
        return mocker.patch(
            'botus_receptus.db.context.select_one', new_callable=mocker.CoroutineMock
        )

    @pytest.fixture
    def mock_search(self, mocker: Mocker) -> Any:
        return mocker.patch(
            'botus_receptus.db.context.search', new_callable=mocker.CoroutineMock
        )

    @pytest.fixture
    def mock_update(self, mocker: Mocker) -> Any:
        return mocker.patch(
            'botus_receptus.db.context.update', new_callable=mocker.CoroutineMock
        )

    @pytest.fixture
    def mock_insert_into(self, mocker: Any) -> Any:
        return mocker.patch(
            'botus_receptus.db.context.insert_into', new_callable=mocker.CoroutineMock
        )

    @pytest.fixture
    def mock_delete_from(self, mocker: Any) -> Any:
        return mocker.patch(
            'botus_receptus.db.context.delete_from', new_callable=mocker.CoroutineMock
        )

    @pytest.mark.asyncio
    async def test_acquire(
        self,
        mocker: Any,
        mock_bot: Any,
        mock_mesage: discord.Message,
        mock_command: typed_commands.Command[Context],
    ) -> None:
        ctx = Context(
            prefix='~', message=mock_mesage, bot=mock_bot, command=mock_command
        )

        async with ctx.acquire():
            assert hasattr(ctx, 'db')
            db = await ctx.acquire()
            assert db == ctx.db
        assert not hasattr(ctx, 'db')

        await ctx.release()

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        mocker: Any,
        mock_bot: Any,
        mock_select_all: Any,
        mock_mesage: discord.Message,
        mock_command: typed_commands.Command[Context],
    ) -> None:
        ctx = Context(
            prefix='~', message=mock_mesage, bot=mock_bot, command=mock_command
        )

        with pytest.raises(RuntimeError):
            await ctx.select_all(table='foo', columns=['col1'])

        async with ctx.acquire():
            await ctx.select_all(table='foo', columns=['col1'])
            mock_select_all.assert_called_once_with(
                ctx.db,
                table='foo',
                columns=['col1'],
                order_by=None,
                where=None,
                joins=None,
                group_by=None,
                record_class=None,
            )

    @pytest.mark.asyncio
    async def test_select_one(
        self,
        mocker: Any,
        mock_bot: Any,
        mock_select_one: Any,
        mock_mesage: discord.Message,
        mock_command: typed_commands.Command[Context],
    ) -> None:
        ctx = Context(
            prefix='~', message=mock_mesage, bot=mock_bot, command=mock_command
        )

        with pytest.raises(RuntimeError):
            await ctx.select_one(table='foo', columns=['col1'])

        async with ctx.acquire():
            await ctx.select_one(table='foo', columns=['col1'])
            mock_select_one.assert_called_once_with(
                ctx.db,
                table='foo',
                columns=['col1'],
                where=None,
                joins=None,
                group_by=None,
                record_class=None,
            )

    @pytest.mark.asyncio
    async def test_search(
        self,
        mocker: Any,
        mock_bot: Any,
        mock_search: Any,
        mock_mesage: discord.Message,
        mock_command: typed_commands.Command[Context],
    ) -> None:
        ctx = Context(
            prefix='~', message=mock_mesage, bot=mock_bot, command=mock_command
        )

        with pytest.raises(RuntimeError):
            await ctx.search(
                table='foo', columns=['col1'], search_columns=['bar'], terms=['baz']
            )

        async with ctx.acquire():
            await ctx.search(
                table='foo', columns=['col1'], search_columns=['bar'], terms=['baz']
            )
            mock_search.assert_called_once_with(
                ctx.db,
                table='foo',
                columns=['col1'],
                search_columns=['bar'],
                terms=['baz'],
                where=None,
                order_by=None,
                joins=None,
                group_by=None,
                record_class=None,
            )

    @pytest.mark.asyncio
    async def test_update(
        self,
        mocker: Any,
        mock_bot: Any,
        mock_update: Any,
        mock_mesage: discord.Message,
        mock_command: typed_commands.Command[Context],
    ) -> None:
        ctx = Context(
            prefix='~', message=mock_mesage, bot=mock_bot, command=mock_command
        )

        with pytest.raises(RuntimeError):
            await ctx.update(table='foo', values={'bar': 'baz'}, where=['spam = "ham"'])

        async with ctx.acquire():
            await ctx.update(table='foo', values={'bar': 'baz'}, where=['spam = "ham"'])
            mock_update.assert_called_once_with(
                ctx.db, table='foo', values={'bar': 'baz'}, where=['spam = "ham"']
            )

    @pytest.mark.asyncio
    async def test_insert_into(
        self,
        mocker: Any,
        mock_bot: Any,
        mock_insert_into: Any,
        mock_mesage: discord.Message,
        mock_command: typed_commands.Command[Context],
    ) -> None:
        ctx = Context(
            prefix='~', message=mock_mesage, bot=mock_bot, command=mock_command
        )

        with pytest.raises(RuntimeError):
            await ctx.insert_into(table='foo', values={'bar': 'baz'})

        async with ctx.acquire():
            await ctx.insert_into(table='foo', values={'bar': 'baz'})
            mock_insert_into.assert_called_once_with(
                ctx.db, table='foo', values={'bar': 'baz'}, extra=''
            )

    @pytest.mark.asyncio
    async def test_delete_from(
        self,
        mocker: Any,
        mock_bot: Any,
        mock_delete_from: Any,
        mock_mesage: discord.Message,
        mock_command: typed_commands.Command[Context],
    ) -> None:
        ctx = Context(
            prefix='~', message=mock_mesage, bot=mock_bot, command=mock_command
        )

        with pytest.raises(RuntimeError):
            await ctx.delete_from(table='foo', where='bar')

        async with ctx.acquire():
            await ctx.delete_from(table='foo', where='bar')
            mock_delete_from.assert_called_once_with(ctx.db, table='foo', where='bar')
