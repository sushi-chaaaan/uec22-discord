import discord
from discord.ext import commands

from newdispanderfixed import dispand


class Message_Sys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message_dispand(self, message: discord.Message):
        avoid_prefix_list = ["!ue "]
        avoid_suffix_list = []
        if type(message.channel) == discord.DMChannel:
            return
        else:
            for prefix in avoid_prefix_list:
                if message.content.startswith(prefix):
                    return
            for suffix in avoid_suffix_list:
                if message.content.endswith(suffix):
                    return
                
            embeds = await dispand(self.bot, message)
            if embeds == []:
                return
            await message.reply(embeds=embeds, mention_author=False)
            return


def setup(bot):
    return bot.add_cog(Message_Sys(bot))
