import asyncio
import traceback
from typing import Optional

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

    @slash_command(name="timer", guild_ids=[guild_id])
    async def _timer(self, ctx: discord.ApplicationContext):
        # get param
        interaction = ctx.interaction
        user = ctx.interaction.user
        channel = ctx.interaction.channel
        if not user or not isinstance(channel, discord.abc.Messageable):
            return

        # get timer
        timer_length = await self.get_timer_length(interaction)

        # set timer
        if not timer_length or not isinstance(timer_length, float):
            return

        # exe timer
        await asyncio.sleep(timer_length)

        # timer_length: 秒単位の数値
        text = f"{user.mention}さん\nタイマーで設定した時間が経過しました。"
        try:
            await channel.send(content=text)
        except Exception:
            traceback.print_exc()

    @slash_command(name="timer-voice", guild_ids=[guild_id])
    async def _timer_voice(self, ctx: discord.ApplicationContext):
        # get param
        interaction = ctx.interaction
        user = ctx.interaction.user
        if not user or not isinstance(user, discord.Member):
            return
        vc_state: Optional[discord.VoiceState] = user.voice

        # reject if user not in vc
        if not vc_state:
            await ctx.respond(
                content="ボイスチャットに参加した状態でないと、このコマンドは使用できません。", ephemeral=True
            )
            return

        # configure timer
        timer_length = await self.get_timer_length(interaction)
        if not timer_length or not isinstance(timer_length, float):
            return

    async def get_timer_length(self, interaction: discord.Interaction) -> float:
        # Send select and determine timer length
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
            timer_length = float(values[0])
        else:
            timer_length = float(res)
        return timer_length


def setup(bot):
    return bot.add_cog(Timer(bot))
