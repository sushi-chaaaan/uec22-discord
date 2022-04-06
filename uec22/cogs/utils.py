from datetime import datetime, timedelta, timezone

import discord
from discord import ApplicationContext, Option
from discord.commands import slash_command
from discord.ext import commands
from ids import guild_id

utc = timezone.utc
jst = timezone(timedelta(hours=9), "Asia/Tokyo")


class Utils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="user", guild_ids=[guild_id])
    async def _newuser(
        self,
        ctx: ApplicationContext,
        member: Option(discord.Member, "対象のIDや名前を入力してください。"),
    ):
        """ユーザー情報を取得できます。"""
        # guild = ctx.guild
        # member = guild.get_member(int(id))
        # この先表示する用
        await ctx.defer()
        member_created: datetime = member.created_at.astimezone(jst)
        created = member_created.strftime("%Y/%m/%d %H:%M:%S")
        member_joined: datetime = member.joined_at.astimezone(jst)
        joined = member_joined.strftime("%Y/%m/%d %H:%M:%S")
        desc = f"対象ユーザー:{member.mention}\nユーザー名:{member}\nID:`{member.id}`\nBot:{member.bot}"
        roles = sorted(member.roles, key=lambda x: x.position, reverse=True)
        send_roles = "\n".join([role.mention for role in roles])
        avatars = [member.avatar, member.display_avatar]
        if member.default_avatar in avatars:
            avatar_url = member.default_avatar.url
        else:
            avatar_url = member.display_avatar.replace(
                size=1024, static_format="webp"
            ).url
        desc = desc + f"\n[Avatar url]({avatar_url})"
        embed = discord.Embed(
            title="ユーザー情報照会結果",
            description=desc,
            color=3983615,
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(
            name="アカウント作成日時",
            value=created,
        )
        embed.add_field(
            name="サーバー参加日時",
            value=joined,
        )
        embed.add_field(name=f"所持ロール({len(roles)})", value=send_roles, inline=False)
        await ctx.respond(embed=embed)
        return


def setup(bot):
    return bot.add_cog(Utils(bot))
