from typing import Any
import discord
import firebase_admin
from discord.ext import commands, tasks
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "data/uec22-discord-firebase-adminsdk-8gyuv-b0189dec6c.json"
)
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_data(collection: str) -> list[dict[Any, Any]]:
    _data = db.collection(collection).get()
    data_model = []
    for data in _data:
        data_model.append(data.to_dict())

    return data_model


class FireStoreTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._check_panel.start()

    def cog_unload(self) -> None:
        self._check_panel.cancel()

    @tasks.loop(hours=12)
    async def _check_panel(self):
        panels = db.collection("role_panel").get()
        for panel in panels:
            _panel = panel.to_dict()
            _guild = await self.bot.fetch_guild(int(_panel["guild_id"]))
            _channel = await _guild.fetch_channel(int(_panel["channel_id"]))
            if not isinstance(_channel, discord.TextChannel):
                print("Invalid ChannelType")
                return
            _message = await _channel.fetch_message(int(_panel["message_id"]))
            if _message is None:
                pass


def setup(bot):
    return bot.add_cog(FireStoreTask(bot))


"""
panels = db.collection("role_panel").get()
for panel in panels:
    print(panel.to_dict())
pass
"""
