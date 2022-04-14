import asyncio
from typing import Optional

import discord
from discord.ui import InputText, Modal


class SelectSender:
    def __init__(self, interaction: discord.Interaction):
        self._interaction = interaction

    async def send(
        self,
        menu_dict: dict[str, str],
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        placeholder: Optional[str] = None,
        min_values: int,
        max_values: int,
        ephemeral: bool = False,
        deffered: bool,
    ) -> tuple[list[str], discord.Interaction]:
        _future = asyncio.Future()
        embed = discord.Embed(
            title=title,
            description=description,
            color=1787875,
        )
        view = self.generate_selectview(
            menu_dict=menu_dict,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            future=_future,
            deferred=deffered,
        )
        await self.respond(embeds=[embed], view=view, ephemeral=ephemeral)
        await _future
        if _future.done():
            return _future.result()

    def generate_selectview(
        self,
        menu_dict: dict[str, str],
        *,
        placeholder: Optional[str],
        min_values: int,
        max_values: int,
        future: asyncio.Future,
        deferred: bool,
    ) -> discord.ui.View:
        view = discord.ui.View(timeout=None)
        options: list[discord.SelectOption] = []
        for key, value in menu_dict.items():
            opt = discord.SelectOption(label=value, value=key)
            options.append(opt)
        select = _Select(
            future=future,
            deferred=deferred,
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
        deferred: bool,
        placeholder: Optional[str] = None,
        min_values: int,
        max_values: int,
        options: list[discord.SelectOption],
    ) -> None:
        super().__init__(
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
        )
        self.future = future
        self.deferred = deferred

    async def callback(self, interaction: discord.Interaction):
        self.future.set_result((self.values, interaction))
        if not self.deferred:
            pass
        else:
            await interaction.response.defer()


class ModalSender:
    def __init__(self, interaction: discord.Interaction):
        self._interaction = interaction

    async def send(
        self,
        modal_list: list[dict],
        *,
        title: str,
        custom_id: Optional[str] = None,
    ) -> tuple[list[str], discord.Interaction]:
        _future = asyncio.Future()
        await self.respond(
            _Modal(future=_future, dicts=modal_list, title=title, custom_id=custom_id)
        )
        await _future
        if _future.done():
            if _future.result() is not None:
                return _future.result()
            raise asyncio.InvalidStateError("Modal was cancelled.")

    @property
    def respond(self):
        if self._interaction.response.is_done():
            raise discord.InteractionResponded(self._interaction)
        else:
            return self._interaction.response.send_modal


class _Modal(Modal):
    def __init__(
        self,
        dicts: list[dict],
        future: asyncio.Future,
        title: str,
        custom_id: Optional[str] = None,
    ) -> None:
        super().__init__(title, custom_id)
        for dict in dicts:
            label = dict["label"]
            if dict["short"]:
                style = discord.InputTextStyle.short
            else:
                style = discord.InputTextStyle.paragraph
            required = dict["required"]
            row = dict["row"]
            value = dict["value"]
            self.add_item(
                InputText(
                    label=label,
                    style=style,
                    required=required,
                    row=row,
                    value=value,
                )
            )
        self.future = future
        self.length = len(dicts)

    async def callback(self, interaction: discord.Interaction):
        values = [self.children[i].value for i in range(self.length)]
        self.future.set_result((values, interaction))
        await interaction.response.defer()
