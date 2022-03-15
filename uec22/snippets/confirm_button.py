import asyncio
import discord
from discord.ui import View
from typing import Optional


class Confirm(View):
    def __init__(
        self,
        future: asyncio.Future,
        custom_id: str,
        timeout: Optional[float] = None,
        label: Optional[str] = None,
    ):
        super().__init__(timeout=timeout)
        self.add_item(
            Confirm_Button(
                mode=True,
                future=future,
                custom_id=custom_id,
                label=label,
            )
        )
        self.add_item(
            Confirm_Button(
                mode=False,
                future=future,
                custom_id=custom_id,
                label=label,
            )
        )


class Accept_Button(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.blurple,
        label: str,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        row: Optional[int] = None,
        future: asyncio.Future,
    ):
        self.future = future
        super().__init__(
            style=style, label=label, disabled=disabled, custom_id=custom_id, row=row
        )

    async def callback(self, interaction: discord.Interaction):
        self.future.set_result([True, interaction])
        await interaction.response.defer()
        await interaction.message.delete()


class Reject_Button(discord.ui.Button):
    def __init__(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.danger,
        label: str,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        row: Optional[int] = None,
        future: asyncio.Future,
    ):
        self.future = future
        super().__init__(
            style=style, label=label, disabled=disabled, custom_id=custom_id, row=row
        )

    async def callback(self, interaction: discord.Interaction):
        self.future.set_result([False, interaction])
        await interaction.response.defer()
        await interaction.message.delete()


class Confirm_Button(discord.ui.Button):
    def __init__(
        self,
        *,
        mode: bool,
        style: Optional[discord.ButtonStyle] = None,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        row: Optional[int] = None,
        future: asyncio.Future,
    ):
        if mode is True:
            _custom_id = f"{custom_id}_accept"
        else:
            _custom_id = f"{custom_id}_reject"
        if style is None:
            if mode is True:
                style = discord.ButtonStyle.blurple
            else:
                style = discord.ButtonStyle.danger
        if label is None:
            if mode is True:
                label = "承認する"
            else:
                label = "承認しない"
        self.mode = mode
        self.future = future
        super().__init__(
            style=style, label=label, disabled=disabled, custom_id=_custom_id, row=row
        )

    async def callback(self, interaction: discord.Interaction):
        self.future.set_result(self.mode)
        await interaction.response.defer()
