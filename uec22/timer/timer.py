import asyncio

import discord
from discord.commands import slash_command
from discord.ext import commands
from ids import guild_id
from uec22.snippets.sender import ModalSender, SelectSender

mode_dict = {
    "600": "10分",
    "1800": "30分",
    "3600": "1時間",
    "other": "その他",
}

modal_dict = [
    {
        "label": "例: 3600(1時間)",
        "short": True,
        "required": True,
        "row": 0,
        "value": None,
    },
]


class Timer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="timer", guild_ids=guild_id)
    async def _timer(self, ctx: discord.ApplicationContext):
        interaction = ctx.interaction
        sender = SelectSender(interaction)
        res, res_interaction = await sender.send(
            menu_dict=mode_dict,
            title="タイマーの長さを選択してください。",
            min_values=1,
            max_values=1,
            ephemeral=True,
            deffered=False,
        )
        res = res[0]
        if res == "other":
            sender = ModalSender(res_interaction)
            values, modal_interaction = await sender.send(
                modal_list=modal_dict,
                title="タイマーの長さを選択してください。(単位: 秒)",
                custom_id="timer_modal",
            )
            timer_length = int(values[0])
        else:
            timer_length = int(res)

        # set timer.
        await asyncio.sleep(timer_length)

        # timer_length: 秒単位の数値


def setup(bot):
    return bot.add_cog(Timer(bot))
