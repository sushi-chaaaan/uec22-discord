from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import discord
from discord import ApplicationContext, Option
from discord.commands import slash_command
from discord.ext import commands
from discord.ext.ui import (
    InteractionProvider,
    Message,
    PageView,
    PaginationView,
    View,
    ViewTracker,
)
from ids import guild_id

thread_log_channel = 963399326992846888
jst = timezone(timedelta(hours=9), "Asia/Tokyo")


class Thread(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_thread_join")
    async def detect_thread(self, thread: discord.Thread):
        members = await thread.fetch_members()
        if self.bot.user.id in [x.id for x in members]:
            return
        embed = self.thread_created(thread)
        guild = self.bot.get_guild(guild_id)
        ch = guild.get_channel(thread_log_channel)
        if not embed or not guild or not isinstance(ch, discord.abc.Messageable):
            return
        await ch.send(embed=embed)

    @commands.Cog.listener(name="on_thread_update")
    async def detect_archive(self, before, after):
        if after.locked and not before.locked:
            return
        elif after.archived and not before.archived:
            await after.edit(archived=False)
            return
        else:
            return

    """
    Thread Board Parts
    normal
    ┣

    bottom
    ┗
    """

    @slash_command(guild_ids=[guild_id], name="board")
    async def _board_slash(
        self,
        ctx: ApplicationContext,
        category: Option(
            discord.CategoryChannel,
            description="対象のカテゴリを選択してください。選択しなかった場合カテゴリのないチャンネルについて実行します。",
            required=False,
        ),
    ):
        if category is not None:
            id = category.id
        else:
            id = None
        board = self._make_board(ctx.interaction, category_id=id)
        await PagePage(text=board)._send(ctx.interaction)
        return

    @staticmethod
    def _make_board(
        interaction: discord.Interaction, category_id: Optional[int] = None
    ) -> str:
        if category_id:
            channels = [
                channel
                for channel in interaction.guild.channels
                if channel.category and channel.category.id == category_id
            ]
        else:
            channels = [
                channel
                for channel in interaction.guild.channels
                if channel.category is None and type(channel) != discord.CategoryChannel
            ]
        trash_vc = [
            channel
            for channel in channels
            if not isinstance(channel, discord.VoiceChannel)
        ]
        sort_channels = sorted(trash_vc, key=lambda channel: channel.position)
        # print(channels)
        thread_dic = {}
        if category_id:
            threads = [
                thread
                for thread in interaction.guild.threads
                if not thread.is_private()
                and not thread.locked
                and thread.parent.category.id == category_id
            ]
        else:
            threads = [
                thread
                for thread in interaction.guild.threads
                if not thread.is_private()
                and not thread.locked
                and thread.parent.category is None
            ]
        # print(threads)
        for thread in threads:
            thread_dic[thread] = thread.parent.position
        """
        thread_dic:
        {thread,
        thread:pos,
        ...}
        """
        final_board = []
        for channel in sort_channels:
            thread_board = [f"<#{channel.id}>"]
            child_thread = sorted(
                [
                    thread
                    for thread, parent_pos in thread_dic.items()
                    if parent_pos == channel.position
                ],
                key=lambda thread: len(thread.name),
            )
            # print(child_thread)
            mark_child_thread = [f"<#{thread.id}>" for thread in child_thread]
            if mark_child_thread:
                board = thread_board + mark_child_thread
                board_text_draft = "\n┣".join(board[:-1])
                board_text = f"{board_text_draft}\n┗{board[-1]}"
                final_board.append(board_text)
            else:
                final_board.append(f"<#{channel.id}>")
        final_text = "\n\n".join(final_board)
        return final_text

    @staticmethod
    def thread_created(thread: discord.Thread):
        if thread.owner is None or thread.parent is None:
            return
        embed = discord.Embed(
            title="New Thread Detected",
            color=1787875,
            timestamp=datetime.now(timezone.utc),
        )
        embed.set_author(
            name=thread.owner.display_name,
            icon_url=thread.owner.display_avatar.url,
        )
        if thread.is_private():
            _status = "Private"
        else:
            _status = "Public"
        embed.add_field(name="Status", value=_status, inline=False)
        embed.add_field(
            name="auto_archive_duration",
            value=thread.auto_archive_duration,
            inline=False,
        )
        embed.add_field(name="parent", value=f"{thread.parent.mention}")
        embed.add_field(name="thread", value=f"{thread.mention}")
        embed.add_field(name="owner", value=f"{thread.owner.mention}")
        embed.add_field(
            name="created_at",
            value=f"{datetime.now(jst).strftime('%Y/%m/%d %H:%M:%S')}",
        )
        return embed


class Page(PageView):
    def __init__(self, text: str):
        super(Page, self).__init__()
        self.text = text

    async def body(self, _paginator: PaginationView) -> Union[Message, View]:
        return Message(content=self.text)

    async def on_appear(self, paginator: PaginationView) -> None:
        pass


class PagePage:
    def __init__(self, text: str) -> None:
        self._text = text
        pass

    def _view(self) -> PaginationView:
        view = PaginationView(
            [
                Page(self._text),
                Page(f"```{self._text}```"),
            ],
            show_indicator=False,
        )
        return view

    async def _send(self, interaction: discord.Interaction):
        view = self._view()
        tracker = ViewTracker(view, timeout=None)
        await tracker.track(InteractionProvider(interaction, ephemeral=True))


def setup(bot):
    return bot.add_cog(Thread(bot))
