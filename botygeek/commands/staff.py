import discord
from botygeek import BotyGeek
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from botygeek.logs import LogType, ClientLogs, ServerLogs



class Staff(commands.Cog):

  bot : BotyGeek
  log : callable

  def __init__(self, bot : BotyGeek):
    self.bot = bot
    self.log = bot.logs.log 

  @commands.command(name="clear")
  async def clear(self, ctx : commands.Context, nb : int):
    async def clear(message : discord.Message):
      if await self._clear(ctx.channel, nb + 2):
        await ClientLogs.deletable(self.bot, ctx, LogType.LogType.VALIDATE, f"Clear of {nb} messages complet", ctx.message.author)

    async def cancel(message : discord.Message):
      await message.delete()
      await ClientLogs.deletable(self.bot, ctx, LogType.LogType.ERROR, f"Clear of {nb} messages cancel", ctx.message.author)

    await ClientLogs.validation(self.bot, ctx, f"Please validate the clear of {nb} messages.", ctx.message.author, clear, cancel, False, 20)
    
  @clear.error
  async def clear_error(self, ctx : commands.Context, error : commands.CommandError):
    if type(error) == MissingRequiredArgument:
      await ClientLogs.helpMessage(
        ctx,
        "clear",
        "delete a specify number of message",
        "clear nb",
        [
          "`nb` *(int)* : number of delete message"
        ]
      )
      return
    self.log(LogType.LogType.ERROR, "CLEAR/ERROR", error)
      
  @staticmethod
  async def _clear(channel : discord.TextChannel, nb : int) -> bool:
    messages = []
    async for x in channel.history(limit = nb):
        messages.append(x)
    await channel.delete_messages(messages)
    return True


  @commands.command(name="ping")
  async def ping(self, ctx : commands.Context):
    await ctx.send("pong")

  @ping.error
  async def ping_error(self, ctx : commands.Context, error : commands.CommandError):
    if type(error) == MissingRequiredArgument:
      await ClientLogs.helpMessage(
        ctx,
        "ping",
        "debug command to view bot ping, send pong",
        "ping"
      )
      return
    self.log(LogType.LogType.ERROR, "PING/ERROR", error)
      
def setup(bot):
  bot.add_cog(Staff(bot))