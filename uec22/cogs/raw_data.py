import os

import discord
from discord.commands import message_command
from discord.ext import commands
from dotenv import load_dotenv

from ids import guild_id

load_dotenv()


class GetRawData(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @message_command(name="get-raw-data", guild_ids=[guild_id])
        async def get_raw_data(
            ctx: discord.ApplicationContext, message: discord.Message
        ):
            await ctx.defer()


def setup(bot):
    return bot.add_cog(GetRawData(bot))
