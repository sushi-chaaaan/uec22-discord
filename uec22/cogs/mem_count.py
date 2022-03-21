import os

from discord.ext import commands, tasks

admin_role = int(os.environ["ADMIN_ROLE"])
count_vc = int(os.environ["COUNT_VC"])
guild_id = int(os.environ["GUILD_ID"])


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
        guild = await self.bot.fetch_guild(guild_id)
        server_member_count = guild.member_count
        vc = self.bot.get_channel(count_vc)
        await vc.edit(name=f"Member Count: {server_member_count}")
        return


def setup(bot):
    return bot.add_cog(MemberCount(bot))
