import discord
from botygeek import BotyGeek
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from botygeek.logs import LogType, ClientLogs, ServerLogs



class Roles(commands.Cog):

  bot : BotyGeek
  log : callable
  theguild : object

  def __init__(self, bot : BotyGeek):
    self.bot = bot
    self.config = bot.config

  @commands.Cog.listener()
  async def on_ready(self):
    self.theguild = self.bot.get_guild(self.config.guildID)


  @commands.Cog.listener()
  async def on_member_join(self, member : discord.Member):
    for id in self.config.roleOnJoin:
      await member.add_roles(member.guild.get_role(id))

  @commands.command(name="getrole")
  async def getrole(self, ctx : commands.Context, rolename : str):
    if isinstance(ctx.channel, discord.DMChannel):
      for id in self.config.roleSelector:
        addrole = self.theguild.get_role(id)
        if str(addrole) == rolename:
          theauthor = self.get_player_by_ID(self, ctx.message.author.id)
          await theauthor.add_roles(addrole)
          await ClientLogs.actionDone(
            ctx,
            "The get gaming role command is done",
            f"You have now the gaming role **{rolename}** on the server __**{self.theguild.name}**__ !",
          )
  
  @commands.command(name="removerole")
  async def removerole(self, ctx : commands.Context, rolename : str):
    if isinstance(ctx.channel, discord.DMChannel):
      for id in self.config.roleSelector:
        addrole = self.theguild.get_role(id)
        if str(addrole) == rolename:
          theauthor = self.get_player_by_ID(self, ctx.message.author.id)
          await theauthor.remove_roles(addrole)
          await ClientLogs.actionDone(
            ctx,
            "The remove gaming role command is done",
            f"You now don't have the gaming role **{rolename}** anymore on the server __**{self.theguild.name}**__ !",
          )

  @getrole.error
  async def getrole_error(self, ctx : commands.Context, error : commands.CommandError):
    if type(error) == MissingRequiredArgument:
      await ClientLogs.helpMessage(
        ctx,
        "Get Role command",
        "Command to add a gaming role and acces to respective channel",
        "getrole <role name> (ex: Minecraft, LOL)"
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
        "removerole <role name> (ex: Minecraft, LOL)"
      )
      return
    self.log(LogType.LogType.ERROR, "REMOVEROLE/ERROR", error)
  
  @staticmethod
  def get_player_by_ID(self, author_id : int):
    return self.theguild.get_member(author_id)

def setup(bot):
  bot.add_cog(Roles(bot))