import traceback

import discord
from discord.ext import commands


class ErrorCatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="err_test")
    async def _err_tst(self, ctx: commands.Context):
        prin("test")

    # called when an error
    @commands.Cog.listener(name="on_error")
    async def _on_err(self, event: str, *args, **kwargs):
        pass

    # called when an error related to discord.ext.commands occurred
    @commands.Cog.listener(name="on_command_error")
    async def _on_cmd_err(self, ctx: commands.Context, error: commands.CommandError):
        # make error ID
        error_id = ctx.message.id
        print(f"on_command_error:\n{error_id}")

        # check error case
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
        content = content + f"\nID: {error_id}"
        try:
            await ctx.reply(content=content)
        except Exception:
            pass
        finally:
            traceback.print_exc()

    # called when an error related in app_command occurred
    @commands.Cog.listener(name="on_application_command_error")
    async def _on_app_cmd_err(
        self, ctx: discord.ApplicationContext, exception: Exception
    ):
        # make error ID
        error_id = ctx.interaction.id
        print(f"app_command_error\nID: {error_id}")

        try:
            await ctx.respond(
                content=f"予期せぬエラーが発生しました。\nID: {error_id}\n\nException: {exception}",
            )
        except Exception:
            pass


def setup(bot):
    return bot.add_cog(ErrorCatch(bot))
