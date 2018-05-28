from typing import Optional, List, Iterable, Union

import discord
from discord.ext import commands
from mypy_extensions import TypedDict
from datetime import datetime


class FooterData(TypedDict, total=False):
    text: str
    icon_url: str


class UrlData(TypedDict, total=False):
    url: str


class AuthorDataBase(TypedDict):
    name: str


class AuthorData(AuthorDataBase, UrlData, total=False):
    icon_url: str


class FieldDataBase(TypedDict):
    name: str
    value: str


class FieldData(FieldDataBase, total=False):
    inline: bool


class EmbedContext(commands.Context):
    async def send_embed(self, description: str, *,
                         title: Optional[str] = None, color: Optional[Union[discord.Color, int]] = None,
                         footer: Optional[Union[str, FooterData]] = None,
                         thumbnail: Optional[str] = None,
                         author: Optional[Union[str, AuthorData]] = None,
                         image: Optional[str] = None,
                         timestamp: Optional[datetime] = None,
                         fields: Optional[List[FieldData]] = None,
                         tts: bool = False, file: Optional[object] = None,
                         files: Optional[List[object]] = None, delete_after: Optional[float] = None,
                         nonce: Optional[int] = None) -> discord.Message:
        embed: discord.Embed = discord.Embed(description=description)

        if title is not None:
            embed.title = title
        if color is not None:
            embed.color = color
        if footer is not None:
            if isinstance(footer, str):
                embed.set_footer(text=footer)
            else:
                embed.set_footer(**footer)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        if author is not None:
            if isinstance(author, str):
                embed.set_author(name=author)
            else:
                embed.set_author(**author)
        if image is not None:
            embed.set_image(url=image)
        if timestamp is not None:
            embed.timestamp = timestamp
        if fields is not None:
            setattr(embed, '_fields', fields)

        return await self.send(tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)


class PaginatedContext(commands.Context):
    async def send_pages(self, pages: Iterable[str], *, tts: bool = False, delete_after: Optional[float] = None,
                         nonce: Optional[int] = None) -> List[discord.Message]:
        return [await self.send(page, tts=tts, delete_after=delete_after, nonce=nonce) for page in pages]