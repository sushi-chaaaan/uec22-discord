import logging
import os
import traceback
import sys

from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands


logging.basicConfig(level=logging.INFO)

utc = timezone.utc
jst = timezone(timedelta(hours=9), "Asia/Tokyo")

token = ""

# Load when start bot
EXTENSION_LIST = [
    "uec22.cogs.error",
    "uec22.cogs.pin",
    "uec22.cogs.role_panel",
]

PERSISTENT_VIEWS = []


# Intent
intents = discord.Intents.default()
intents.typing = False


class MyBot(commands.Bot):
    def __init__(self, command_prefix="!ue", **options):
        super().__init__(command_prefix, intents=intents, **options)
        self.persistent_views_added = False
        for cog in EXTENSION_LIST:
            try:
                self.load_extension(cog)
                print(f"Extension [{cog}.py] is loaded!")
            except Exception:
                traceback.print_exc()

    # run when boot is done preparing to run.
    async def on_ready(self):
        if not self.persistent_views_added:
            for view in PERSISTENT_VIEWS:
                try:
                    self.add_view(view)
                    print(f"Added View [{view}] !")
                except Exception:
                    traceback.print_exc()
            self.persistent_views_added = True
        info = ""
        if self.user is None:
            info = "cannot get my own infomation."
        else:
            info = f"Logged in as {self.user} (ID:{self.user.id})\nNow: {discord.utils.utcnow().astimezone(jst).strftime('%Y/%m/%d %H:%M:%S')}\nLibrary version: {discord.__version__}\nPython Info:{sys.version}"
        print("------------------------------------------------------")
        print(info)
        print("------------------------------------------------------")
        channel = self.get_channel(951165574237532200)
        if isinstance(channel, discord.TextChannel):
            await channel.send(f"```{info}```")
        else:
            print("Failed to send boot message: Invalid ChannelType")


bot = MyBot()

if __name__ == "__main__":
    bot.run(token)
