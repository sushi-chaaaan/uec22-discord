import os
import traceback
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands


class ErrorCatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_error")
    async def _on_err(self, event: str, *args, **kwargs):
        pass

    @commands.Cog.listener(name="on_command_error")
    async def _on_cmd_err(self, ctx: commands.Context, err: commands.CommandError):
        pass
