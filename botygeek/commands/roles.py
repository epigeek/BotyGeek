import discord
from botygeek import BotyGeek
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from botygeek.logs import LogType, ClientLogs, ServerLogs



class Roles(commands.Cog):

  bot : BotyGeek
  log : callable

  def __init__(self, bot : BotyGeek):
    self.bot = bot
    self.config = bot.config

  @commands.Cog.listener()
  async def on_member_join(self, member : discord.Member):
    for id in self.config.roleOnJoin:
      await member.add_roles(member.guild.get_role(id))

  @commands.command(name="getrole")
  async def getrole(self, ctx : commands.Context, rolename : str):
    for id in self.config.roleSelector:
      addrole = ctx.guild.get_role(id)
      if str(addrole) == rolename:
        await ctx.author.add_roles(addrole)
  
  @commands.command(name="removerole")
  async def removerole(self, ctx : commands.Context, rolename : str):
    for id in self.config.roleSelector:
      removerole = ctx.guild.get_role(id)
      if str(removerole) == rolename:
        await ctx.author.remove_roles(removerole)

  @getrole.error
  async def getrole_error(self, ctx : commands.Context, error : commands.CommandError):
    if type(error) == MissingRequiredArgument:
      await ClientLogs.helpMessage(
        ctx,
        "Get Role command",
        "Command to add a gaming role and acces to respective channel",
        "getrole <role name>"
      )
      return
    self.log(LogType.LogType.ERROR, "GETROLE/ERROR", error)
  
  @removerole.error
  async def removerole_error(self, ctx : commands.Context, error : commands.CommandError):
    if type(error) == MissingRequiredArgument:
      await ClientLogs.helpMessage(
        ctx,
        "Remove Role command",
        "Command to remove a gaming role and acces to respective channel",
        "removerole <role name>"
      )
      return
    self.log(LogType.LogType.ERROR, "REMOVEROLE/ERROR", error)


def setup(bot):
  bot.add_cog(Roles(bot))