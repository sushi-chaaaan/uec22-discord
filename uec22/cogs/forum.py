import discord
from discord.ext import commands

from ids import forum_start_ch,forum_category


class Forum(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def forum_start(self, message: discord.Message):
        if message.author.bot or isinstance(message.channel, discord.DMChannel) or isinstance(message.channel,discord.GroupChannel):
            return
        if message.channel.id != forum_start_ch or message.channel.category_id != forum_category or message.channel.category is None:
            return
        else:
            title = message.content
            cat = message.guild.get_channel(forum_category)
            if not isinstance(cat,discord.CategoryChannel):
                return
            await cat.create_text_channel(name=title)

    @commands.Cog.listener(name="on_message")
    async def forum_close


def setup(bot):
    return bot.add_cog(Forum(bot))
