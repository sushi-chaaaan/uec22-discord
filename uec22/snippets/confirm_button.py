import asyncio
from typing import Optional

import discord

# 基本的に await asyncio.Future()な形で運用する前提です。ボタンはbool(承認/非承認結果)とinteractionオブジェクトのタプルを返します。
# 基本的にConfirmViewをそのままつかってください


class ConfirmView(discord.ui.View):
    def __init__(
        self,
        label_ok: str,
        label_ng: str,
        future: Optional[asyncio.Future] = None,
        disabled: bool = False,
        timeout: Optional[float] = None,
    ):
        super().__init__(timeout=timeout)
        self.add_item(
            Accept_Button(
                label=label_ok, future=future, disabled=disabled,
            )
        )
        self.add_item(
            Reject_Button(
                label=label_ng, future=future, disabled=disabled,
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
        future: Optional[asyncio.Future] = None,
    ):
        self.future = future
        super().__init__(
            style=style, label=label, disabled=disabled, custom_id=custom_id, row=row
        )

    async def callback(self, interaction: discord.Interaction):
        if self.future:
            self.future.set_result([True, interaction])
        await interaction.response.defer()
        if interaction.message:
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
        future: Optional[asyncio.Future] = None,
    ):
        self.future = future
        super().__init__(
            style=style, label=label, disabled=disabled, custom_id=custom_id, row=row
        )

    async def callback(self, interaction: discord.Interaction):
        if self.future:
            self.future.set_result([False, interaction])
        await interaction.response.defer()
        if interaction.message:
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
