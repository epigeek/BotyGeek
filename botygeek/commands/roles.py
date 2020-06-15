import discord
from botygeek import BotyGeek
from botygeek.config.Config import Config
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from botygeek.logs import LogType, ClientLogs, ServerLogs
from typing import List


class Roles(commands.Cog):

  bot : BotyGeek
  config : Config
  log : callable
  guild : discord.Guild
  roleSelector : List[discord.Role]
  roleOnJoin : List[discord.Role]

  def __init__(self, bot : BotyGeek):
    self.bot = bot
    self.config = bot.config
    self.log = bot.logs.log
    self.guild = None
    self.roleSelector = []
    self.roleOnJoin = []

  @commands.Cog.listener()
  async def on_ready(self):
    self.guild = self.bot.get_guild(self.config.serverID)
    self.roleSelector = Roles.getRolesByIDList(self.guild, self.config.roleSelector)
    self.roleOnJoin = Roles.getRolesByIDList(self.guild, self.config.roleOnJoin)

  @commands.Cog.listener()
  async def on_member_join(self, member : discord.Member):
    for role in self.roleOnJoin:
      await member.add_roles(role)

  @commands.command(name="addrole")
  async def addrole(self, ctx : commands.Context, rolename : str):
    if not isinstance(ctx.channel, discord.DMChannel):
      return
    role : discord.Role = self.getSelectorRoleByName(rolename)
    if not role:
      await ClientLogs.send(
        ctx,
        LogType.LogType.ERROR,
        "Role not can't be added",
        f"**{rolename}** roles didn't exist\n" + self.possibleChoice()
      )
      return
    member : discord.Member = self.getMemblerByUser(ctx.author)
    if not member:
      await ClientLogs.send(
        ctx,
        LogType.LogType.ERROR,
        "Role not can't be added",
        "you are not in the server"
      )
      return
    await member.add_roles(role)
    await ClientLogs.send(
      ctx,
      LogType.LogType.VALIDATE,
      "Role successfully added",
      f"You have now the **{rolename}** role!"
    )

  @addrole.error
  async def addrole_error(self, ctx : commands.Context, error : commands.CommandError):
    if type(error) == MissingRequiredArgument:
      await ClientLogs.helpMessage(
        ctx,
        "add Role",
        "get the roles given as parameter in the server",
        "addrole <role name>",
        [
          "`role name` *(str)* : the role you want have\n" + self.possibleChoice()
        ]
      )
      return
    self.log(LogType.LogType.ERROR, "ADDROLE/ERROR", error)

  @commands.command(name="removerole")
  async def removeRole(self, ctx : commands.Context, rolename : str):
    if not isinstance(ctx.channel, discord.DMChannel):
      return
    role : discord.Role = self.getSelectorRoleByName(rolename)
    if not role:
      await ClientLogs.send(
        ctx,
        LogType.LogType.ERROR,
        "Role not can't be removed",
        f"**{rolename}** roles didn't exist\n" + self.possibleChoice()
      )
      return
    member : discord.Member = self.getMemblerByUser(ctx.author)
    if not member:
      await ClientLogs.send(
        ctx,
        LogType.LogType.ERROR,
        "Role not can't be removed",
        "you are not in the server"
      )
      return
    await member.add_roles(role)
    await ClientLogs.send(
      ctx,
      LogType.LogType.VALIDATE,
      "Role successfully removed",
      f"You didn't have the **{rolename}** role anymore !",
    )


  @removeRole.error
  async def removeRole_error(self, ctx : commands.Context, error : commands.CommandError):
    if type(error) == MissingRequiredArgument:
      await ClientLogs.helpMessage(
        ctx,
        "remove Role",
        "remove the roles given as parameter in the server",
        "removerole <role name>",
        [
          "`role name` *(str)* : the role you not longer wan't\n" + self.possibleChoice()
        ]
      )
      return
    self.log(LogType.LogType.ERROR, "REMOVEROLE/ERROR", error)

  def getSelectorRoleByName(self, name : str) -> discord.Role:
    if not self.guild:
      return
    for id in self.config.roleSelector:
        role : discord.Role = self.guild.get_role(id)
        if role.name == name:
          return role

  @staticmethod
  def getRolesByIDList(guild : discord.Guild, ids : list) -> discord.Role:
    roles = []
    for id in ids:
      role : discord.Role = guild.get_role(id)
      if role:
        roles.append(role)
    return roles

  def getMemblerByUser(self, user : discord.User) -> discord.Member:
    return self.guild.get_member(user.id)


  def possibleChoice(self) -> str:
    message = "**Possible Choice :**"
    for role in self.roleSelector:
      message += f"\n- {role.name}"
    return message


def setup(bot):
  bot.add_cog(Roles(bot))