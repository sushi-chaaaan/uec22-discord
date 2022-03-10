import os
import traceback
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands


class ErrorCatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_error")
    async def _on_err(self, event: str, *args, **kwargs):
        pass

    @commands.Cog.listener(name="on_command_error")
    async def _on_cmd_err(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            content = f"コマンドの実行に必要なパラメータが指定されていません。\n不足したパラメータ:{error.param.name}"
        elif isinstance(error, commands.BadArgument):
            content = "不適切なパラメータが指定されました。"
        elif isinstance(error, commands.PrivateMessageOnly):
            content = "このコマンドはDMでしか実行できません。"
        elif isinstance(error, commands.CommandNotFound):
            content = "指定されたコマンドは存在しません。"
        elif isinstance(error, commands.TooManyArguments):
            content = "指定されたパラメータが多すぎます。"
        elif isinstance(error, commands.CommandOnCooldown):
            content = f"このコマンドは一時的に使用できません。\n{error.retry_after}秒以上待ってからもう一度お試しください。"
        elif isinstance(error, commands.MessageNotFound):
            content = f"指定されたメッセージを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.MemberNotFound):
            content = f"指定されたメンバーを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.GuildNotFound):
            content = f"指定されたサーバーを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.UserNotFound):
            content = f"指定されたユーザーを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.ChannelNotFound):
            content = f"指定されたメンバーを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.ChannelNotReadable):
            content = f"指定されたチャンネルにアクセスする権限がありません。\n```{error.argument}```"
        elif isinstance(error, commands.ThreadNotFound):
            content = f"指定されたスレッドを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.RoleNotFound):
            content = f"指定されたロールを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.EmojiNotFound):
            content = f"指定された絵文字を取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.GuildStickerNotFound):
            content = f"指定されたステッカーを取得できませんでした。\n```{error.argument}```"
        elif isinstance(error, commands.MissingPermissions):
            perms = "\n".join(error.missing_permissions)
            content = f"Botの権限が不足しています。\n```{perms}```"
        else:
            content = f"不明なエラーが発生しました。\n```{error}```"
        try:
            await ctx.reply(content=content)
        except Exception:
            traceback.print_exc()
