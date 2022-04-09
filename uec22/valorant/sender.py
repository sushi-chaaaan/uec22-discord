import asyncio
from typing import Optional

import discord


class InteractionSelectSender:
    def __init__(self, interaction: discord.Interaction, menu_dict: dict[str, str]):
        self._interaction = interaction
        self._menu_dict = menu_dict

    async def send(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        placeholder: Optional[str] = None,
        min_values: int,
        max_values: int,
        ephemeral: bool = False
    ) -> tuple[list[str], discord.Interaction]:
        _future = asyncio.Future()
        embed = discord.Embed(
            title=title,
            description=description,
            color=1787875,
        )
        view = self.generate_selectview(
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            future=_future,
        )
        await self.respond(embeds=[embed], view=view, ephemeral=ephemeral)
        await _future
        if _future.done():
            return _future.result()

    def generate_selectview(
        self,
        placeholder: Optional[str],
        min_values: int,
        max_values: int,
        future: asyncio.Future,
    ) -> discord.ui.View:
        view = discord.ui.View(timeout=None)
        options: list[discord.SelectOption] = []
        for key, value in self._menu_dict.items():
            opt = discord.SelectOption(label=value, value=key)
            options.append(opt)
        select = _Select(
            future=future,
            placeholder=placeholder,
            options=options,
            min_values=min_values,
            max_values=max_values,
        )
        view.add_item(select)
        return view

    @property
    def respond(self):
        if not self._interaction.response.is_done():
            return self._interaction.response.send_message
        else:
            return self._interaction.followup.send


class _Select(discord.ui.Select):
    def __init__(
        self,
        *,
        future: asyncio.Future,
        placeholder: Optional[str] = None,
        min_values: int,
        max_values: int,
        options: list[discord.SelectOption]
    ) -> None:
        super().__init__(
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
        )
        self.future = future

    async def callback(self, interaction: discord.Interaction):
        self.future.set_result((self.values, interaction))
        await interaction.response.defer()
