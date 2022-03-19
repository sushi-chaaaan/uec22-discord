from discord.ext import commands
from typing import Any

from uec22.role_panel.role_panel import RolePanelView


async def set_board(bot: commands.Bot, panel: dict[Any, Any]) -> None:
    _guild = await bot.fetch_guild(int(panel["guild_id"]))
    _roles = []
    for num in range(5):
        _role_id = panel[f"role_{num+1}"]
        if _role_id == "":
            continue
        _role = _guild.get_role(int(panel[f"role_{num+1}"]))
        if _role is not None:
            _roles.append(_role)
        else:
            continue
    bot.add_view(RolePanelView(roles=_roles), message_id=int(panel["message_id"]))
