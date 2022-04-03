from discord.ext import commands, tasks
from ids import guild_id

count_vc = 959628458718289961


class MemberCount(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_count.start()

    def cog_unload(self):
        self.start_count.cancel()

    @tasks.loop(minutes=30.0)
    async def start_count(self):
        await self.membercount()

    @start_count.before_loop
    async def before_count(self):
        await self.bot.wait_until_ready()

    async def membercount(self):
        guild = self.bot.get_guild(guild_id)
        server_member_count = guild.member_count
        vc = self.bot.get_channel(count_vc)
        await vc.edit(name=f"Member Count: {server_member_count}")


def setup(bot):
    return bot.add_cog(MemberCount(bot))
