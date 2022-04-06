from typing import Optional

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

    @slash_command(guild_ids=[guild_id], name="genshin-register")
    async def g_register_id(
        self,
        ctx: ApplicationContext,
        gen_uid: Option(
            str,
            description="原神のUID",
        ),
    ):
        """原神のUIDをDiscordアカウントと紐つけます。"""
        await ctx.defer()
        if not ctx.interaction.user:
            return
        user = ctx.interaction.user
        # make dict
        db_dict = {
            "genshin_id": int(gen_uid),
            "discord_id": user.id,
        }
        # add to DB
        add_data(collection="genshin_id", document=str(user.id), data=db_dict)
        await ctx.interaction.followup.send(
            content=f"UID: `{gen_uid}` を登録しました。", ephemeral=True
        )
        return

    @slash_command(guild_ids=[guild_id], name="genshin-search")
    async def g_search_id(
        self,
        ctx: ApplicationContext,
        target: Option(discord.Member, description="検索するユーザー"),
    ):
        """Discordアカウントと紐づいた原神のUIDを検索します。"""
        await ctx.defer()
        if not ctx.interaction.user:
            return
        # Get Data Frame
        df = self.get_frame(collection="genshin_id")
        # Search
        if target:
            res = self.search_by_id(df=df, target=target.id)
            if res:
                await ctx.interaction.followup.send(
                    content=f"{target}さんの原神UIDは{str(res)}です", ephemeral=True
                )
                return
            else:
                await ctx.interaction.followup.send(
                    content=f"{target}さんのUIDは登録されていません", ephemeral=True
                )
                return

    def search_by_id(self, df: pd.DataFrame, target: int) -> Optional[int]:
        res_df = df[df["discord_id"] == target]
        if res_df.empty:
            return None
        else:
            return res_df["genshin_id"].values[0]

    @slash_command(guild_ids=[guild_id], name="genshin-delete")
    async def g_delete_id(
        self,
        ctx: ApplicationContext,
    ):
        """Discordアカウントと紐づいた原神のUIDを削除します。"""
        await ctx.defer()
        if not ctx.interaction.user:
            return
        target = ctx.interaction.user
        if target:
            delete_data(collection="genshin_id", document=str(target.id))
            await ctx.interaction.followup.send(
                content=f"{target}さんのUIDを削除しました", ephemeral=True
            )
            return
        else:
            await ctx.interaction.followup.send(
                content="削除するユーザーを指定してください", ephemeral=True
            )
            return


def setup(bot):
    return bot.add_cog(GenshinID(bot))
