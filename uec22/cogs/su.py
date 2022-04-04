import asyncio

import discord
from discord.ext import commands
from ids import admin_role, su_role


class SuperUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="su")
    @commands.has_role(admin_role)
    @commands.guild_only()
    async def _su(self, ctx: commands.Context):
        target = ctx.message.author
        guild = ctx.guild()
        if not isinstance(target, discord.Member) or not guild:
            return
        if su_role not in [r.id for r in target.roles]:
            # su権限を持っていない
            _su_role = guild.get_role(su_role)
            if not _su_role:
                print("Cannot find su Role")
                return
            await target.add_roles(_su_role)
            await ctx.reply(content="su権限を付与しました。300秒後に解除されます。")
            await asyncio.sleep(300)
            await target.remove_roles(_su_role)
            return
        # su権限をすでに持っている
        await ctx.reply(content="既にsu権限を所持しています。")
        return


def setup(bot):
    return bot.add_cog(SuperUser(bot))
