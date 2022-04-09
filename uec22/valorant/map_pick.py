import asyncio
import random

import discord
from discord import ApplicationContext, Option
from discord.commands import slash_command
from discord.ext import commands
from ids import guild_id

from .sender import InteractionSelectSender

map_dict = {
    "1": "Ascent",
    "2": "Split",
    "3": "Fracture",
    "4": "Bind",
    "5": "Breeze",
    "6": "Icebox",
    "7": "Haven",
}

side_dict = {
    "attack": "攻撃側",
    "defend": "防衛側",
}


class MapPick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="valorant-pick-map", guild_ids=[guild_id])
    async def _map_pick(
        self,
        ctx: ApplicationContext,
        mode: Option(str, "モードを選択してください。", choices=["BO1", "BO3"]),
        leader_1: Option(discord.Member, "一人目のリーダーを選択してください。"),
        leader_2: Option(discord.Member, "二人目のリーダーを選択してください。"),
    ):
        """MAPのPick/BANを開始します。"""
        embed = discord.Embed(
            title=f"マップ選択システム(モード: {mode})",
            color=1787875,
            description=f"マップのPick/BANを開始します。\n\n{leader_1.mention}さんがチームAボタンを押した後、\n{leader_2.mention}さんはチームBボタンを押してください。\n\n押す順番やボタンを間違えると正しく動作しないことがあります。",
        )
        atk_future = asyncio.Future()
        def_future = asyncio.Future()
        await ctx.respond(embeds=[embed], view=StartPickview(atk_future, def_future))
        await atk_future
        await def_future
        if atk_future.done() is True and def_future.done() is True:
            atk_interaction = atk_future.result()
            def_interaction = def_future.result()
            leaders = {
                "atk": atk_interaction.user,
                "def": def_interaction.user,
            }
            if mode == "BO1":
                atk_sender = InteractionSelectSender(
                    interaction=atk_interaction, menu_dict=map_dict
                )
                atk_ban, atk_ban_interaction = await atk_sender.send(
                    title="BANするマップを2つ選択してください。",
                    min_values=2,
                    max_values=2,
                    ephemeral=True,
                )
                map_pool = {k: v for k, v in map_dict.items() if k not in atk_ban}
                def_sender = InteractionSelectSender(
                    interaction=def_interaction, menu_dict=map_pool
                )
                def_ban, def_ban_interaction = await def_sender.send(
                    title="BANするマップを2つ選択してください。",
                    min_values=2,
                    max_values=2,
                    ephemeral=True,
                )
                map_pool = {k: v for k, v in map_pool.items() if k not in def_ban}
                atk_pick_sender = InteractionSelectSender(
                    interaction=atk_ban_interaction, menu_dict=map_pool
                )
                selected_map, atk_pick_interaction = await atk_pick_sender.send(
                    title="使用するマップを選択してください。",
                    min_values=1,
                    max_values=1,
                    ephemeral=True,
                )
                selected_map = map_dict[selected_map[0]]
                leader_list = [leaders["atk"], leaders["def"]]
                attacker_side = random.choice(leader_list)
                leader_list.remove(attacker_side)
                embed = discord.Embed(
                    title="マップとサイドが決定しました。",
                    color=1787875,
                )
                embed.add_field(
                    name="マップ",
                    value=f"{selected_map}",
                    inline=False,
                )
                embed.add_field(
                    name="攻撃側",
                    value=f"{attacker_side.mention}さんのチーム",
                    inline=False,
                )
                embed.add_field(
                    name="防衛側",
                    value=f"{leader_list[0].mention}さんのチーム",
                    inline=False,
                )
                await atk_interaction.followup.send(embeds=[embed])
                return
            elif mode == "BO3":
                atk_sender = InteractionSelectSender(
                    interaction=atk_interaction, menu_dict=map_dict
                )
                atk_ban, atk_ban_interaction = await atk_sender.send(
                    title="BANするマップを1つ選択してください。",
                    min_values=1,
                    max_values=1,
                    ephemeral=True,
                )
                map_pool = {k: v for k, v in map_dict.items() if k not in atk_ban}
                def_sender = InteractionSelectSender(
                    interaction=def_interaction, menu_dict=map_pool
                )
                def_ban, def_ban_interaction = await def_sender.send(
                    title="BANするマップを1つ選択してください。",
                    min_values=1,
                    max_values=1,
                    ephemeral=True,
                )
                map_pool = {k: v for k, v in map_pool.items() if k not in def_ban}
                # get map1
                atk_pick_sender = InteractionSelectSender(
                    interaction=atk_ban_interaction, menu_dict=map_pool
                )
                selected_map_1, atk_pick_interaction = await atk_pick_sender.send(
                    title="第1マップを選択してください。",
                    min_values=1,
                    max_values=1,
                    ephemeral=True,
                )
                map_pool = {
                    k: v for k, v in map_pool.items() if k not in selected_map_1
                }
                selected_map_1 = map_dict[selected_map_1[0]]
                # get map1 side
                def_decide_side_map1_sender = InteractionSelectSender(
                    interaction=def_ban_interaction, menu_dict=side_dict
                )
                (
                    def_map1_side,
                    def_decide_side_map1_interaction,
                ) = await def_decide_side_map1_sender.send(
                    title="第1マップが決定しました。",
                    description=f"第1マップ: {selected_map_1}",
                    placeholder="第1マップのサイドを選択してください。",
                    min_values=1,
                    max_values=1,
                    ephemeral=True,
                )
                def_map1_side = side_dict[def_map1_side[0]]
                # get map2
                def_pick_map2_sender = InteractionSelectSender(
                    interaction=def_ban_interaction, menu_dict=map_pool
                )
                (
                    selected_map_2,
                    def_pick_map2_interaction,
                ) = await def_pick_map2_sender.send(
                    title="第2マップを選択してください。", min_values=1, max_values=1, ephemeral=True
                )
                map_pool = {
                    k: v for k, v in map_pool.items() if k not in selected_map_2
                }
                selected_map_2 = map_dict[selected_map_2[0]]
                # get map2 side
                atk_decide_side_map2_sender = InteractionSelectSender(
                    interaction=atk_pick_interaction, menu_dict=side_dict
                )
                (
                    atk_map2_side,
                    atk_decide_side_map2_interaction,
                ) = await atk_decide_side_map2_sender.send(
                    title="第2マップが決定しました。",
                    description=f"第2マップ: {selected_map_2}",
                    placeholder="第2マップのサイドを選択してください。",
                    min_values=1,
                    max_values=1,
                    ephemeral=True,
                )
                atk_map2_side = side_dict[atk_map2_side[0]]
                # get map3
                def_pick_map3_sender = InteractionSelectSender(
                    interaction=def_pick_map2_interaction, menu_dict=map_pool
                )
                (
                    selected_map_3,
                    def_pick_map3_interaction,
                ) = await def_pick_map3_sender.send(
                    title="第3マップを選択してください。", min_values=1, max_values=1, ephemeral=True
                )
                map_pool = {
                    k: v for k, v in map_pool.items() if k not in selected_map_3
                }
                selected_map_3 = map_dict[selected_map_3[0]]
                # get map3 side
                atk_decide_side_map3_sender = InteractionSelectSender(
                    interaction=atk_decide_side_map2_interaction, menu_dict=side_dict
                )
                (
                    atk_map3_side,
                    atk_decide_side_map3_interaction,
                ) = await atk_decide_side_map3_sender.send(
                    title="第3マップが決定しました。",
                    description=f"第3マップ: {selected_map_3}",
                    placeholder="第3マップのサイドを選択してください。",
                    min_values=1,
                    max_values=1,
                    ephemeral=True,
                )
                atk_map3_side = side_dict[atk_map3_side[0]]
                final_embeds = []
                final_embed_1 = discord.Embed(
                    title="マップとサイドが決定しました。",
                    color=1787875,
                )
                final_embeds.append(final_embed_1)
                embed_map1 = discord.Embed(
                    title="第1マップ",
                    description=f"マップ: {selected_map_1}\n\nPicked by: {atk_pick_interaction.user.mention}",
                    color=1787875,
                )
                if def_map1_side == "attack":
                    embed_map1.add_field(
                        name="攻撃側", value=leaders["def"].mention, inline=False
                    )
                    embed_map1.add_field(
                        name="防衛側", value=leaders["atk"].mention, inline=False
                    )
                else:
                    embed_map1.add_field(
                        name="攻撃側", value=leaders["atk"].mention, inline=False
                    )
                    embed_map1.add_field(
                        name="防衛側", value=leaders["def"].mention, inline=False
                    )
                final_embeds.append(embed_map1)
                embed_map2 = discord.Embed(
                    title="第2マップ",
                    description=f"マップ: {selected_map_2}\n\nPicked by: {def_pick_map2_interaction.user.mention}",
                    color=1787875,
                )
                if atk_map2_side == "attack":
                    embed_map2.add_field(
                        name="攻撃側", value=leaders["atk"].mention, inline=False
                    )
                    embed_map2.add_field(
                        name="防衛側", value=leaders["def"].mention, inline=False
                    )
                else:
                    embed_map2.add_field(
                        name="攻撃側", value=leaders["def"].mention, inline=False
                    )
                    embed_map2.add_field(
                        name="防衛側", value=leaders["atk"].mention, inline=False
                    )
                final_embeds.append(embed_map2)
                embed_map3 = discord.Embed(
                    title="第3マップ",
                    description=f"マップ: {selected_map_3}\n\nPicked by: {def_pick_map3_interaction.user.mention}",
                    color=1787875,
                )
                if atk_map3_side == "attack":
                    embed_map3.add_field(
                        name="攻撃側", value=leaders["atk"].mention, inline=False
                    )
                    embed_map3.add_field(
                        name="防衛側", value=leaders["def"].mention, inline=False
                    )
                else:
                    embed_map3.add_field(
                        name="攻撃側", value=leaders["def"].mention, inline=False
                    )
                    embed_map3.add_field(
                        name="防衛側", value=leaders["atk"].mention, inline=False
                    )
                final_embeds.append(embed_map3)
                await atk_interaction.followup.send(embeds=final_embeds)
                return


class StartPickview(discord.ui.View):
    def __init__(
        self,
        atk_future: asyncio.Future,
        def_future: asyncio.Future,
    ):
        super().__init__(timeout=None)
        self._atk = atk_future
        self._def = def_future

    @discord.ui.button(label="チームA", style=discord.ButtonStyle.danger)
    async def _attack(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self._atk.set_result(interaction)
        await interaction.response.defer()

    @discord.ui.button(label="チームB", style=discord.ButtonStyle.success)
    async def _defend(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self._def.set_result(interaction)
        await interaction.response.defer()


def setup(bot):
    return bot.add_cog(MapPick(bot))
