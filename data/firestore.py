import traceback
from typing import Any, Optional

import discord
import firebase_admin
from discord.ext import commands, tasks
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate(
        r"data/uec22-discord-firebase-adminsdk-8gyuv-b0189dec6c.json"
    )
    firebase_admin.initialize_app(cred)
db = firestore.client()


def get_data(collection: str) -> Optional[list[dict[Any, Any]]]:
    try:
        _data = db.collection(collection).get()
    except Exception:
        traceback.print_exc()
        return
    data_model = []
    for data in _data:
        data_model.append(data.to_dict())

    return data_model


def add_data(collection: str, document: str, data: dict):
    try:
        db.collection(collection).document(document).set(data)
    except Exception:
        traceback.print_exc()


def delete_data(collection: str, document: str):
    try:
        db.collection(collection).document(document).delete()
    except Exception:
        traceback.print_exc()


class FireStoreTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_panel.start()

    def cog_unload(self) -> None:
        self.check_panel.cancel()

    @tasks.loop(hours=6)
    async def check_panel(self):
        panels: Optional[list[dict[Any, Any]]] = get_data(collection="role_panel")
        if panels is None:
            print("Check Panel Error")
            return
        for panel in panels:
            _guild = self.bot.get_guild(int(panel["guild_id"]))
            if _guild is None:
                delete_data(collection="role_panel", document=panel["message_id"])
                continue
            _ch = _guild.get_channel_or_thread(int(panel["channel_id"]))
            if _ch is None or not isinstance(_ch, discord.abc.Messageable):
                delete_data(collection="role_panel", document=panel["message_id"])
                continue
            _msg = _ch.get_partial_message(int(panel["message_id"]))
            if _msg is None:
                delete_data(collection="role_panel", document=panel["message_id"])
                continue
            else:
                pass

    @check_panel.before_loop
    async def before_check_panel(self):
        print("DB Check: Waiting for Bot")
        await self.bot.wait_until_ready()


def setup(bot):
    return bot.add_cog(FireStoreTask(bot))
