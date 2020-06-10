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


def setup(bot):
  bot.add_cog(Roles(bot))