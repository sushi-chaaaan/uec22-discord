import subprocess
from pathlib import Path
from subprocess import CompletedProcess

import discord
from discord.commands import slash_command
from discord.ext import commands
from ids import guild_id


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
        result = self.convert_md_to_pdf(f"tmp/{attachment.filename}")
        status = "成功" if result.returncode == 0 else "失敗"
        await ctx.respond(f"{result.args}の実行に{status}しました\n\n{result.stdout}")

    def convert_md_to_pdf(self, filename: str) -> CompletedProcess:
        pure_name = filename.removesuffix(".md")
        return subprocess.run(
            f"npx markdown-pdf {filename} -o {pure_name}.pdf -s styles/github-markdown.css",
        )


def setup(bot):
    return bot.add_cog(MarkdownPDF(bot))
