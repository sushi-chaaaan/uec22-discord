from email import message
import logging
import os
import traceback
import sys

from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands

from uec22.role_panel.role_panel_old import RolePanel
from data.firestore import db


logging.basicConfig(level=logging.INFO)

utc = timezone.utc
jst = timezone(timedelta(hours=9), "Asia/Tokyo")

token = ""

# Load when start bot
EXTENSION_LIST = [
    "uec22.cogs.error",
    "uec22.cogs.pin",
    "uec22.role_panel.role_panel",
]

PERSISTENT_VIEWS = []

ROLE_PANEL = [RolePanel]

discord.http.API_VERSION = 9

# Intent
intents = discord.Intents.default()
intents.typing = False


class MyBot(commands.Bot):
    def __init__(self, command_prefix="!ue ", **options):
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
            panels = db.collection("role_panel").get()
            for panel in panels:
                panel = panel.to_dict()
                _guild = await self.fetch_guild(int(panel["guild_id"]))
                _roles = []
                _role_1 = _guild.get_role(int(panel["role_1"]))
                _roles.append(_role_1)
                self.add_view(
                    RolePanel(roles=_roles), message_id=int(panel["message_id"])
                )
            self.persistent_views_added = True
        info = ""
        if self.user is None:
            info = "cannot get my own infomation."
        else:
            info = f"Logged in as {self.user} (ID:{self.user.id})\nNow: {datetime.now(jst).strftime('%Y/%m/%d %H:%M:%S')}\nLibrary version: {discord.__version__}\nPython Info:{sys.version}"
        print("------------------------------------------------------")
        print(info)
        print("------------------------------------------------------")
        channel = self.get_channel(951165574237532200)
        if isinstance(channel, discord.TextChannel):
            await channel.send(f"```{info}```")
        else:
            print("Failed to send boot message: Invalid ChannelType")
        panels = db.collection("role_panel").get()
        for panel in panels:
            print(panel.to_dict())


bot = MyBot()

if __name__ == "__main__":
    bot.run(token)
