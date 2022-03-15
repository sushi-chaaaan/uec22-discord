import asyncio
import discord
from typing import Optional


# 基本的に await asyncio.Future()な形で運用する前提です。
# いい感じにViewに Accept_ButtonとReject_Buttonをくっつけてあげてください


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
        if interaction.message is not None:
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
        if interaction.message is not None:
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
