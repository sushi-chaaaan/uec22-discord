import logging
import sys
import traceback
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import discord
from discord.ext import commands

from data.firestore import get_data
from ids import guild_id, su_role
from uec22.cogs.entrance import EnterVerifyView
from uec22.cogs.forum import QuestionView
from uec22.role_panel.panel_db import set_board

logging.basicConfig(level=logging.INFO)

utc = timezone.utc
jst = timezone(timedelta(hours=9), "Asia/Tokyo")

token = ""

# Load when start bot
EXTENSION_LIST = [
    "data.firestore",
    "uec22.cogs.entrance",
    "uec22.cogs.error",
    "uec22.cogs.forum",
    "uec22.cogs.markdown2pdf",
    "uec22.cogs.mem_count",
    "uec22.cogs.message",
    "uec22.cogs.pin",
    "uec22.cogs.poll",
    "uec22.cogs.su",
    "uec22.cogs.thread",
    "uec22.cogs.utils",
    "uec22.genshin.connect_id",
    "uec22.role_panel.role_panel",
    "uec22.timer.timer",
    "uec22.valorant.map_pick",
]


discord.http.API_VERSION = 9

# Intent
intents = discord.Intents.all()
intents.typing = False


# Bot Constructor
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

        # Set View
        if not self.persistent_views_added:
            PERSISTENT_VIEWS = [
                QuestionView(),
                EnterVerifyView(),
            ]
            for view in PERSISTENT_VIEWS:
                try:
                    self.add_view(view)
                    print(f"Added View [{view}] !")
                except Exception:
                    traceback.print_exc()
            # list[dict[Any, Any]]
            panels: Optional[list[dict[Any, Any]]] = get_data(collection="role_panel")
            if panels is None:
                pass
            else:
                for panel in panels:
                    await set_board(self, panel)
            self.persistent_views_added = True

        # Disarm superuser
        guild = self.get_guild(guild_id)
        if not guild:
            return
        su = guild.get_role(su_role)
        if not su or not su.members:
            return
        for mem in su.members:
            await mem.remove_roles(su)
        print("Disarmed superuser!")

        # Send ready message
        if self.user is None:
            info = "cannot get my own infomation."
        else:
            info = f"Logged in as {self.user} (ID:{self.user.id})\nNow: {datetime.now(jst).strftime('%Y/%m/%d %H:%M:%S')}\nLibrary version: {discord.__version__}\nPython Info:{sys.version}"
        print("------------------------------------------------------")
        print(info)
        print("------------------------------------------------------")
        channel = self.get_channel(959849216052723882)
        if isinstance(channel, discord.abc.Messageable):
            await channel.send(f"```{info}```")
        else:
            print("Failed to send boot message: Invalid ChannelType")


bot = MyBot()

if __name__ == "__main__":
    bot.run(token)
