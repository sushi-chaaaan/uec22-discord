import asyncio
from random import random

import discord
from discord import ApplicationContext, Option
from discord.commands import slash_command
from discord.ext import commands
from ids import guild_id

map_dict = {
    "1": "Ascent",
    "2": "Split",
    "3": "Fracture",
    "4": "Bind",
    "5": "Breeze",
    "6": "Icebox",
    "7": "Haven",
}


class MapPick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="map-pick", guild_ids=[guild_id])
    async def _map_pick(
        self,
        ctx: ApplicationContext,
        mode: Option(str, "モードを選択してください。", choices=["BO1", "BO3"]),
    ):
        """MAPのPick/BANを開始します。"""
        embed = discord.Embed(
            title="マップ選択システム",
            color=1787875,
            description="マップのPick/Banを開始します。\n攻撃側・防衛側各一人ずつがボタンを\n押して指示に従ってください。",
        )
        atk_future = asyncio.Future()
        def_future = asyncio.Future()
        if mode == "BO1":
            await ctx.respond(
                embeds=[embed], view=StartPickview_BO1(atk_future, def_future)
            )
            await atk_future
            await def_future
            if atk_future.done() is True and def_future.done() is True:
                await ctx.respond("入力を確認")
                atk_values, atk_interaction = atk_future.result()
                def_values, def_interaction = def_future.result()
                decided_map = decide_map(map_dict, atk_values, def_values)
                embed = discord.Embed(
                    title="MAPが決定しました。",
                    description=f"使用MAP: {decided_map}",
                    color=1787875,
                )
                await atk_interaction.followup.send(embeds=[embed])
                return
            await ctx.respond("BO3に近日対応予定です。")


def decide_map(map_dict: dict[str, str], atk_values: list, def_values: list) -> str:
    values = atk_values + def_values
    set_values = set(values)
    map_pool = [v for k, v in map_dict.items() if k not in set_values]
    decided_map = random.choice(map_pool)
    return decided_map


class StartPickview_BO1(discord.ui.View):
    def __init__(self, atk_future: asyncio.Future, def_future: asyncio.Future):
        super().__init__(timeout=None)
        self._atk = atk_future
        self._def = def_future

    @discord.ui.button(label="攻撃側", style=discord.ButtonStyle.danger)
    async def _attack(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        view = discord.ui.View(timeout=None)
        view.add_item(MapBanSelect(self._atk, custom_id="atk_map_select"))
        await interaction.response.send_message(
            "BANするマップを2つ選択してください。", view=view, ephemeral=True
        )

    @discord.ui.button(label="防御側", style=discord.ButtonStyle.success)
    async def _defend(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        view = discord.ui.View(timeout=None)
        view.add_item(MapBanSelect(self._def, custom_id="def_map_select"))
        await interaction.response.send_message(
            "BANするマップを2つ選択してください。", view=view, ephemeral=True
        )


def generate_select_from_dict(map_dict: dict) -> list[discord.SelectOption]:
    options: list[discord.SelectOption] = []
    for key, value in map_dict.items():
        opt = discord.SelectOption(label=value, value=key)
        options.append(opt)
    return options


class MapBanSelect(discord.ui.Select):
    def __init__(
        self,
        future: asyncio.Future,
        *,
        custom_id: str,
        placeholder: str = "BANするマップを2つ選択してください。",
        min_values: int = 2,
        max_values: int = 2,
    ) -> None:
        options = generate_select_from_dict(map_dict)
        super().__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
        )
        self.future = future

    async def callback(self, interaction: discord.Interaction):
        # return list of selected values and interaction
        self.future.set_result([[self.values], interaction])
        await interaction.response.defer()


def setup(bot):
    return bot.add_cog(MapPick(bot))
