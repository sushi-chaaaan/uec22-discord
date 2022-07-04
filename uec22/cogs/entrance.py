import discord
from discord import Embed
from discord.ext import commands

from ids import student


class Entrance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="send-ent")
    @commands.has_permissions(administrator=True)
    async def _ent_cmd(self, ctx: commands.Context):
        await ctx.send(embeds=[self.ent_embed()], view=EnterVerifyView())

    @staticmethod
    def ent_embed() -> Embed:
        embed = Embed(
            color=1787875,
            title="ようこそ",
            description="入室ボタンを押してください。",
        )
        return embed


class EnterVerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="入室",
        custom_id="entrance_button",
        style=discord.ButtonStyle.blurple,
        row=0,
    )
    async def _ent(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.guild and isinstance(interaction.user, discord.Member):
            role = interaction.guild.get_role(student)
            if role:
                await interaction.user.add_roles(role)
        await interaction.response.send_message(
            content="UEC22 Discordへようこそ！\nまずは<#959628711139901470>を見てください！",
            ephemeral=True,
        )
        return


def setup(bot):
    return bot.add_cog(Entrance(bot))
