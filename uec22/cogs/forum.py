import asyncio
from typing import Optional

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import InputText, Modal
from ids import forum_category, forum_start_ch


class Forum(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="quetest")
    async def _que(self, ctx: commands.Context):
        await ctx.send(view=QuestionView())


class QuestionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="質問する！",
        custom_id="question_sys_button",
        style=discord.ButtonStyle.blurple,
        emoji="<:help_white:957274506618077194>",
    )
    async def question_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        future = asyncio.Future()
        await interaction.response.send_modal(QuestionModal(future=future))
        await future
        if future.done():
            title, _interaction = future.result()
            cat = interaction.channel.category
            if cat:
                q_ch = await cat.create_text_channel(name=title)
                await _interaction.followup.send(content=q_ch.mention)
            else:
                return


class QuestionModal(Modal):
    def __init__(
        self,
        future: asyncio.Future,
        title: str = "質問システム",
        custom_id: Optional[str] = None,
    ) -> None:
        super().__init__(title, custom_id)
        self.add_item(
            InputText(
                style=discord.InputTextStyle.short,
                label="質問タイトル",
                placeholder="〇〇がわからない、〇〇について知りたい",
            )
        )
        self.future = future

    async def callback(self, interaction: discord.Interaction):
        self.future.set_result((self.children[0].value, interaction))
        await interaction.response.defer()


class ForumEmbed:
    def start_button(self) -> Embed:
        pass


def setup(bot):
    return bot.add_cog(Forum(bot))
