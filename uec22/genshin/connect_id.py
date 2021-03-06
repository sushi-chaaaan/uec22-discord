import math
from typing import Optional

import discord
import pandas as pd
from discord import ApplicationContext, Option
from discord.commands import slash_command
from discord.ext import commands

from data.firestore import add_data, delete_data, get_data
from ids import guild_id


class GenshinID(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def get_frame(collection: str) -> pd.DataFrame:
        """create DataFrame from FireStore"""
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
        await ctx.respond(f"UID: `{gen_uid}` を登録しました。", ephemeral=True)
        return

    @slash_command(guild_ids=[guild_id], name="genshin-search")
    async def g_search_id(
        self,
        ctx: ApplicationContext,
        target: Option(discord.Member, description="検索するユーザー"),
    ):
        """Discordアカウントと紐づいた原神のUIDを検索します。"""
        if not ctx.interaction.user:
            return
        # Get Data Frame
        df = self.get_frame(collection="genshin_id")
        # Search
        if target:
            res = self.search_by_id(df=df, target=target.id)
            if res:
                res = math.floor(res)
                await ctx.respond(
                    f"{target.mention}さんの原神UIDは{str(res)}です", ephemeral=True
                )
                return
            else:
                await ctx.respond(f"{target.mention}さんのUIDは登録されていません", ephemeral=True)
                return

    @slash_command(guild_ids=[guild_id], name="genshin-search-all")
    async def g_search_all(
        self,
        ctx: ApplicationContext,
    ):
        """Discordアカウントと紐づいた原神のUIDの一覧を返します。"""
        if not ctx.interaction.user:
            return
        # Get Data Frame
        df = self.get_frame(collection="genshin_id")
        # Search
        res = self.search_all(df=df)
        if res:
            id_text_list = [
                f"<@!{d['discord_id']}>さんのUID: {d['genshin_id']}" for d in res
            ]
            send_text = "\n".join(id_text_list)
            embed = discord.Embed(
                title="原神UIDリスト",
                description=send_text,
                color=1787875,
            )
            await ctx.respond(embeds=[embed], ephemeral=True)
        else:
            await ctx.respond("UIDリストを出力できませんでした。", ephemeral=True)
            return

    @staticmethod
    def search_all(df: pd.DataFrame) -> list[dict[str, int]]:
        """Create list of dict from DataFrame"""
        id_list = []
        for row in df.itertuples():
            discord_id = row.discord_id
            genshin_id = row.genshin_id
            _dict = {
                "genshin_id": genshin_id,
                "discord_id": discord_id,
            }
            id_list.append(_dict)
        return id_list

    @staticmethod
    def search_by_id(df: pd.DataFrame, target: int) -> Optional[int]:
        """Search bindded UID from Discord ID"""
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
        if not ctx.interaction.user:
            return
        target = ctx.interaction.user
        if target:
            delete_data(collection="genshin_id", document=str(target.id))
            await ctx.respond(f"{target.mention}さんのUIDを削除しました", ephemeral=True)
            return


def setup(bot):
    return bot.add_cog(GenshinID(bot))
