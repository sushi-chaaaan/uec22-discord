from discord.ext import commands, tasks
from ids import guild_id

count_vc = 955434095490510949


class MemberCount(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_count.start()

    def cog_unload(self):
        self.start_count.cancel()

    @tasks.loop(minutes=30)
    async def start_count(self):
        await self.bot.wait_until_ready()
        await self.membercount()

    async def membercount(self):
        guild = self.bot.get_guild(guild_id)
        server_member_count = guild.member_count
        vc = self.bot.get_channel(count_vc)
        await vc.edit(name=f"Member Count: {server_member_count}")
        return


def setup(bot):
    return bot.add_cog(MemberCount(bot))
