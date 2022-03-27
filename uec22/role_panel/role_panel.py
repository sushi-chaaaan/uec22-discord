import asyncio
from typing import Optional

import discord
from data.firestore import add_data
from discord import Embed
from discord.ext import commands
from discord.ui import InputText, Modal
from uec22.snippets.confirm_button import ConfirmView


class RolePanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # パネル作成コマンド
    @commands.command(name="role-panel")
    @commands.guild_only()
    async def _role_panel(
        self,
        ctx: commands.Context,
        target: Optional[discord.TextChannel] = None,
        *role_id: str,
    ):
        # check param
        if target is None:
            await ctx.reply(content="送信先チャンネルの指定が必要です。")
            return
        if role_id == []:
            await ctx.reply(content="パネルに載せるロールが最低一つ必要です。")
            return
        if len(role_id) > 6:
            await ctx.reply(
                content="一度に指定できるロールの数は5つまでです。\n6つ以上指定したい場合は、2つ以上のパネルに分けてください。"
            )
            return
        # get role
        roles = [ctx.guild.get_role(int(role)) for role in role_id]
        if roles == []:
            await ctx.reply(content="ロールの取得時にエラーが発生しました。")
            return
        # prepare board
        modal_future = asyncio.Future()
        view = PanelModalView(future=modal_future)
        await ctx.send(embeds=[PanelEmbed().start()], view=view)
        # check send board
        await modal_future
        if modal_future.done() is True:
            _title, text, modal_interaction = modal_future.result()
            panel_embed = PanelEmbed()._panel(_title, text)
            test_role_view = RolePanelView(roles=roles, disabled=True)
            # send test panel
            await modal_interaction.followup.send(
                content=f"この内容で{target.mention}にロールパネルを作成しますか？",
                embeds=[panel_embed],
                view=test_role_view,
            )
            conf_msg = await modal_interaction.original_message()
            conf_future = asyncio.Future()
            conf_view = ConfirmView(
                label_ok="作成する", label_ng="作成しない", future=conf_future
            )
            # confirm
            await conf_msg.reply(view=conf_view)
            await conf_future
            if conf_future.done() is True:
                conf_result, conf_interaction = conf_future.result()
                # send board
                if conf_result is True:
                    panel_view = RolePanelView(roles=roles)
                    panel_msg: discord.Message = await target.send(
                        embeds=[panel_embed], view=panel_view
                    )
                    await conf_msg.reply(
                        embeds=[
                            PanelEmbed()._panel_accept(
                                target=target, url=panel_msg.jump_url
                            )
                        ]
                    )
                    # prepare data for DB
                    db_dict = {
                        "guild_id": str(ctx.guild.id),
                        "channel_id": str(panel_msg.channel.id),
                        "message_id": str(panel_msg.id),
                    }
                    for num in range(5):
                        try:
                            db_dict[f"role_{num+1}"] = role_id[num]
                        except Exception:
                            db_dict[f"role_{num+1}"] = ""
                    set_data(message_id=str(panel_msg.id), data=db_dict)
                    # await conf_msg.reply("uploaded to DB")
                    # upload to DB
                else:
                    # cancel
                    await conf_interaction.message.delete()
                    await conf_msg.reply(content="パネルの作成をキャンセルしました。")


def set_data(message_id: str, data: dict) -> None:
    add_data(collection="role_panel", document=message_id, data=data)


# 作成確認用View


# パネル説明入力View
class PanelModalView(discord.ui.View):
    def __init__(self, future: asyncio.Future):
        self.future = future
        super().__init__(timeout=None)
        pass

    @discord.ui.button(label="入力", style=discord.ButtonStyle.blurple)
    async def panel_modal(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_modal(RolePanelModal(future=self.future))


# パネル説明入力用Modal
class RolePanelModal(Modal):
    def __init__(self, future: asyncio.Future) -> None:
        self.future = future
        super().__init__(title="ロールパネルメッセージ入力")
        self.add_item(
            InputText(
                label="パネルタイトル(必要に応じて変更してください)",
                style=discord.InputTextStyle.short,
                required=True,
                value="ロールパネル",
                row=0,
            )
        )
        self.add_item(
            InputText(
                label="パネルメッセージ",
                style=discord.InputTextStyle.paragraph,
                required=True,
                row=1,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        self.future.set_result(
            (self.children[0].value, self.children[1].value, interaction)
        )
        await interaction.response.defer()


# ロールパネル本体のView
class RolePanelView(discord.ui.View):
    def __init__(self, roles: list[discord.Role], disabled: bool = False):
        super().__init__(timeout=None)
        role_buttons = [RoleButton(role, disabled=disabled) for role in roles]
        for button in role_buttons:
            self.add_item(button)


# ロールパネルのボタン
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
        if not isinstance(user, discord.Member):
            print("TypeError in Make Role Button")
            return
        if self.role not in user.roles:
            await user.add_roles(self.role)
            embed = RoleEmbed(self.role).add_embed()
            await interaction.response.send_message(embeds=[embed], ephemeral=True)
        else:
            await user.remove_roles(self.role)
            embed = RoleEmbed(self.role).remove_embed()
            await interaction.response.send_message(embeds=[embed], ephemeral=True)


# ここから下はEmbedObjectを作るやつ
class PanelEmbed:
    def start(self) -> Embed:
        embed = Embed(
            title="ロールパネル作成",
            color=1787875,
            description="下のボタンを押して、\nロールパネルに載せる説明を入力してください。\nこのテキストのように表示されます。",
        )
        return embed

    def _panel(
        self, title: str, text: str, footer: str = "付与/解除したいロールのボタンを押してください。"
    ) -> Embed:
        embed = Embed(
            title=title,
            description=text,
            color=1787875,
        )
        embed.set_footer(text=footer)
        return embed

    def _panel_accept(self, target: discord.TextChannel, url: str) -> Embed:
        embed = Embed(
            title="作成完了",
            color=1787875,
            description=f"{target.mention}にロールパネルを作成しました。",
            url=url,
        )
        return embed


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


# Cogとして追加
def setup(bot):
    return bot.add_cog(RolePanel(bot))
