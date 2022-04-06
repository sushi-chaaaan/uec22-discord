import discord
from data.firestore import db
from typing import Optional


from discord.ext import commands


def get_panel_data() -> list[dict[str, str]]:
    _panels = db.collection("role_panel").get()
    raw_panels: list[dict[str, str]] = [_panel.to_dict() for _panel in _panels]

    # panel:
    # {'guild_id': '951133867157385256', 'message_id': '952453563869704192', 'role_1': '951884383067967498', 'role_4': '', 'role_3': '', 'role_2': '', 'role_5': ''}

    return raw_panels


class FireStoreCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def purse_data(_panel_dict: dict[str, str]):
        guild_id = int(_panel_dict["guild_id"])
        channel_id = int(_panel_dict["channel_id"])
        message_id = int(_panel_dict["message_id"])
        _raw_roles: list[str] = [
            _panel_dict["role_1"],
            _panel_dict["role_2"],
            _panel_dict["role_3"],
            _panel_dict["role_4"],
            _panel_dict["role_5"],
        ]
        role_ids: list[int] = []
        for raw_role in _raw_roles:
            if raw_role != "":
                role_ids.append(int(raw_role))

    async def _get_role(self, gu_id: int, role_ids: list[int]) -> list[discord.Role]:
        guild = await self.bot.fetch_guild(gu_id)
        roles: list[discord.Role] = []
        for id in role_ids:
            _role = guild.get_role(id)
            if _role is not None:
                roles.append(_role)
        return roles


def setup(bot):
    return bot.add_cog(FireStoreCog(bot))
