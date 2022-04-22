import subprocess
from subprocess import CompletedProcess

import discord
from discord.commands import slash_command
from discord.ext import commands
from ids import guild_id
from test_md import md2html_md_to_pdf


class MarkdownPDF(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(name="markdown-pdf", guild_ids=[guild_id])
    async def markdown_pdf(
        self,
        ctx: discord.ApplicationContext,
        attachment: discord.Option(
            discord.Attachment,
            "変換するmarkdownファイル",
            required=True,
        ),
    ):
        await ctx.defer()
        print(attachment.filename)
        await attachment.save(f"tmp/{attachment.filename}")
        pure_name = attachment.filename.removesuffix(".md")
        result = md2html_md_to_pdf(f"tmp/{attachment.filename}")
        if not result:
            await ctx.respond("実行に失敗しました")
            return
        await ctx.respond(f"{pure_name}.pdfを作成しました。", file=discord.File(result))


def setup(bot):
    return bot.add_cog(MarkdownPDF(bot))
