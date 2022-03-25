from typing import Any

import discord
import pandas as pd
from data.firestore import add_data, delete_data, get_data
from discord import ApplicationContext, Option
from discord.commands import slash_command
from discord.ext import commands

from ids import guild_id


class GenshinID(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_frame(self, collection: str) -> pd.DataFrame:
        _data = get_data(collection=collection)
        return pd.json_normalize(_data)

    @slash_command(guild_ids=[guild_id], name="g-connect")
    async def g_register_id(
        self,
        ctx: ApplicationContext,
        gen_uid: Option(
            str,
            description="原神のUID",
        ),
    ):
        await ctx.defer()
        if not ctx.interaction.user:
            return
        user = ctx.interaction.user
        # Get Data Frame
        df = self.get_frame(collection="genshin_id")
        print(df)
        # search by Discord ID
        res_df = df[df["discord_id"] == str(user.id)]
        # Output ID (type:str)
        g_id = res_df["genshin_id"].values[0]

    @slash_command(guild_ids=[guild_id], name="g-search")
    async def g_search_id(
        self,
        ctx: ApplicationContext,
        target: Option(discord.Member, description="検索するユーザー"),
    ):
        await ctx.defer()
        if not ctx.interaction.user:
            return
        # Get Data Frame

        df = self.get_frame(collection="genshin_id")
        # print(df)
        # search by Discord ID

        res_df = df[df["discord_id"] == str(target.id)]
        # print(res_df)
        # Output ID (type: str)

        g_id = res_df["genshin_id"].values[0]
        # print(g_id)
        await ctx.interaction.followup.send(content=f"{target}さんの原神UIDは{g_id}です")


def setup(bot):
    return bot.add_cog(GenshinID(bot))
