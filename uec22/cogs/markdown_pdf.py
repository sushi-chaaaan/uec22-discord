import json
import subprocess

import discord
from discord.commands import slash_command
from discord.ext import commands

from ids import guild_id


class MDPDF(commands.Cog):
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
        result = self.md2html_md_to_pdf(f"tmp/{attachment.filename}")
        if not result:
            await ctx.respond("実行に失敗しました")
            return
        await ctx.respond(f"{pure_name}.pdfを作成しました。", file=discord.File(result))

    def md2html_md_to_pdf(self, filename: str) -> str | None:
        pure_name = filename.removesuffix(".md")
        marked_opt = '{"gfm": true}'
        marked_json = json.dumps(marked_opt)
        pdf_opt = '{"format": "A4", "margin": "15mm", "printBackground": true}'
        pdt_json = json.dumps(pdf_opt)
        launch_opt = '{"args": ["--no-sandbox","--disable-setuid-sandbox"],"executablePath": "/usr/bin/google-chrome-stable"}'
        launch_json = json.dumps(launch_opt)
        try:
            subprocess.run(
                f"npx md-to-pdf --stylesheet styles/github-markdown.css --highlight-style github --marked-options {marked_json} --launch-options {launch_json} --pdf-options {pdt_json} {filename}",
                shell=True,
            )
        except subprocess.CalledProcessError as e:
            print(e)
        else:
            return f"{pure_name}.pdf"


def setup(bot):
    return bot.add_cog(MDPDF(bot))
