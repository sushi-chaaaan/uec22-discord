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

CORE_EXTENSION_LIST = []

PERSISTENT_VIEWS = []

token = ""


class MyBot(commands.Bot):
    def __init__(self, command_prefix="!ue", **options):
        super().__init__(command_prefix, **options)
        self.persistent_views_added = False
        for cog in CORE_EXTENSION_LIST:
            try:
                self.load_extension(cog)
                print(f"Extension [{cog}.py] is loaded!")
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        if not self.persistent_views_added:
            for view in PERSISTENT_VIEWS:
                try:
                    self.add_view(view)
                    print(f"Added View {view} !")
                except Exception:
                    traceback.print_exc()
            self.persistent_views_added = True
        info = f"Logged in as {self.user} (ID:{self.user.id})\nNow: {datetime.utcnow().astimezone(jst).strftime('%Y/%m/%d %H:%M:%S')}\nLibrary version: {discord.__version__}\nPython Info:{sys.version}"
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
