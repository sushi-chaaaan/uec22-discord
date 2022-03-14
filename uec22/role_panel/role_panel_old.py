import asyncio
import traceback
from typing import Optional

import discord
from discord.ext import commands
from discord.ui import InputText, Modal


class ReactRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="role-panel")
    async def _role_panel(
        self,
        ctx: commands.Context,
        target: Optional[discord.TextChannel] = None,
        *role_id: str,
    ):
        if target is None:
            await ctx.reply(content="送信先チャンネルのIDを指定してください。")
            return
        if len(role_id) > 6:
            await ctx.reply(
                content="一度に指定できるロールの数は5つまでです。\n6つ以上指定したい場合は、２つ以上のパネルに分けてください。"
            )
            return
        roles = [ctx.guild.get_role(int(role)) for role in role_id]

        # make modal button
        modal_view = PanelModal(roles, target)
        await ctx.reply(content="ボタンを押してパネルの説明を入力してください。", view=modal_view)
        pass


class PanelModal(discord.ui.View):
    def __init__(self, roles: list[discord.Role], target: discord.TextChannel):
        self.roles = roles
        self.target = target
        super().__init__(timeout=None)
        pass

    @discord.ui.button(label="パネルメッセージ入力", style=discord.ButtonStyle.blurple)
    async def panel_modal(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_modal(
            RolePanelModal(roles=self.roles, target=self.target)
        )


class RolePanelModal(Modal):
    def __init__(self, roles: list[discord.Role], target: discord.TextChannel) -> None:
        self.roles = roles
        self.target = target
        super().__init__(title="ロールパネルメッセージ入力")
        self.add_item(
            InputText(
                label="パネルメッセージ",
                style=discord.InputTextStyle.paragraph,
                required=True,
                row=1,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        # make button View(disabled)
        _panel_view = Dis_RolePanel(roles=self.roles)
        panel_view = RolePanel(roles=self.roles)
        embed = discord.Embed(
            title="ロールパネル",
            description=self.children[0].value,
            color=3447003,
        )
        embed.set_footer(text="付与/解除したいロールのボタンを押してください。")
        await interaction.response.send_message(
            content="以下の内容でロールパネルを作成しますか？", embeds=[embed], view=_panel_view
        )
        message: discord.Message = await interaction.original_message()
        future = asyncio.Future()
        await message.reply(view=Confirm(future=future))
        await future
        if future.done():
            if future.result() is True:
                await self.target.send(embeds=[embed], view=panel_view)
            else:
                pass
            return


class Confirm(discord.ui.View):
    def __init__(self, future: asyncio.Future):
        self.future = future
        super().__init__(timeout=None)

    @discord.ui.button(
        label="する", custom_id="role_panel_accept", style=discord.ButtonStyle.blurple
    )
    async def _accept(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.future.set_result(True)
        await interaction.message.edit(view=Dis_Confirm())
        await interaction.response.send_message(content="ロールパネルの作成を開始します。")
        return

    @discord.ui.button(
        label="しない", custom_id="role_panel_reject", style=discord.ButtonStyle.blurple
    )
    async def _reject(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.future.set_result(False)
        await interaction.response.send_message(content="ロールパネルの作成をキャンセルしました。")
        await interaction.message.delete(delay=None)


class Dis_Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="する", style=discord.ButtonStyle.blurple, disabled=True)
    async def _accept(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        pass

    @discord.ui.button(label="しない", style=discord.ButtonStyle.blurple, disabled=True)
    async def _reject(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        pass


class RolePanel(discord.ui.View):
    def __init__(self, roles: Optional[list[discord.Role]] = None):
        super().__init__(timeout=None)
        if roles is not None:
            role_buttons = [RoleButton(role) for role in roles]
            for button in role_buttons:
                self.add_item(button)


class Dis_RolePanel(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        role_buttons = [RoleButton(role, disabled=True) for role in roles]
        super().__init__(timeout=None)
        for button in role_buttons:
            self.add_item(button)


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, **kwargs):
        self.role = role
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label=role.name,
            custom_id=f"role_button_{role.id}",
            **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if self.role not in user.roles:
            await user.add_roles(self.role)
            embed = RoleEmbed(self.role).add_embed()
            await interaction.response.send_message(embeds=[embed], ephemeral=True)
        else:
            await user.remove_roles(self.role)
            embed = RoleEmbed(self.role).remove_embed()
            await interaction.response.send_message(embeds=[embed], ephemeral=True)


class RoleEmbed:
    def __init__(self, role: discord.Role) -> None:
        self.role = role

    def add_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="ロール付与完了",
            description=f"{self.role.mention} を付与しました。\nロールを外したい場合はもう一度\nロールのボタンを押すことで外すことが可能です。",
            color=3447003,
        )
        return embed

    def remove_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="ロール解除完了",
            description=f"{self.role.mention} を解除しました。\nロールを再度付与したい場合はもう一度ロールのボタンを押すことで再度付与することが可能です。",
            color=3447003,
        )
        return embed


def setup(bot):
    return bot.add_cog(ReactRole(bot))
