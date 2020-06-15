import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, CommandError
from botygeek import BotyGeek
from botygeek.logs.LogType import LogType



class Track(commands.Cog):

  bot : BotyGeek

  def __init__(self, bot : BotyGeek):
    self.bot = bot
    self.log = bot.logs.log

  # COMMAND
  @commands.Cog.listener()
  async def on_command_error(self, ctx : commands.Context, error : CommandError):
    return

  # CONNECTION
  @commands.Cog.listener()
  async def on_connect(self):
    self.log(LogType.VALIDATE, "CONNECT", f"{self.bot.user} {self.bot.user.id}")

  @commands.Cog.listener()
  async def on_disconnect(self):
    self.log(LogType.WARNING, "DISCONNECT", f"{self.bot.user} {self.bot.user.id}")

  @commands.Cog.listener()
  async def on_ready(self):
    self.log(LogType.INFO, "READY", f"Discord.API {discord.__version__}, Extension : {self.bot.initial_extensions}")

  @commands.Cog.listener()
  async def on_resumed(self):
    self.log(LogType.INFO, "RECONNECT", f"{self.bot.user} {self.bot.user.id}")



  ###############
  #   MESSAGE   #
  ###############
  @commands.Cog.listener()
  async def on_message(self, message : discord.Message):
    if message.author != self.bot.user:
      self.log(LogType.INFO, f"MESSAGE/NEW/{self._getMessagePath(message)}" , self._getMessageContent(message))

  @commands.Cog.listener()
  async def on_message_delete(self, message : discord.Message):
    if message.author != self.bot.user:
      self.log(LogType.WARNING, f"MESSAGE/DELETE/{self._getMessagePath(message)}" , self._getMessageContent(message))

  @commands.Cog.listener()
  async def on_message_edit(self, before : discord.Message, after : discord.Message):
    if before.author == self.bot.user:
      return
    if before.content != after.content:
      await self._on_message_content_edit(before, after)
    elif before.embeds != after.embeds:
      await self._on_message_embeds_edit(before, after)
    elif before.pinned != after.pinned:
      await self._on_message_pin(after)
    # TODO : add other type : https://discordpy.readthedocs.io/en/latest/api.html#discord.on_message_edit

  async def _on_message_content_edit(self, before : discord.Message, after : discord.Message):
    self.log(LogType.WARNING, f"MESSAGE/EDIT/{self._getMessagePath(before)}" , f"{self._getMessageContent(before, True, False)} -> {self._getMessageContent(after, False)}")

  async def _on_message_embeds_edit(self, before : discord.Message, after : discord.Message):
    pass

  async def _on_message_pin(self, message : discord.Message):
    self.log(LogType.WARNING, f"MESSAGE/"+ ("PIN" if message.pinned else "UNPIN") + f"/{self._getMessagePath(message)}" , self._getMessageContent(message))


  @staticmethod
  def _getMessagePath(message : discord.Message) -> str:
    if isinstance(message.channel, discord.TextChannel):
      return f"PUBLIC/{message.channel}"
    else:
      return f"PRIVATE/{message.author.name}"

  @staticmethod
  def _getMessageContent(message : discord.Message, author : bool = True, messageId : bool = True) -> str:
    content = f'{message.author.name}({message.author.id}) : ' if author else ''
    content += f'"{message.content}"'
    if len(message.attachments):
      content += " : "
      for attachment in message.attachments:
        content += attachment.url
    if messageId:
      content += f" ({message.channel.id}/{message.id})"
    return content

  ###############
  #   REATION   #
  ###############
  @commands.Cog.listener()
  async def on_reaction_add(self, reaction : discord.Reaction, user : discord.User):
    message = reaction.message
    if message.author != self.bot.user:
      self.log(LogType.INFO, f"REACTION/ADD/{self._getMessagePath(message)}" , f"{user.name}({user.id}) : {self._getEmoji(reaction.emoji)} -> {self._getMessageContent(message)}")

  @commands.Cog.listener()
  async def on_reaction_remove(self, reaction : discord.Reaction, user : discord.User):
    message = reaction.message
    if message.author != self.bot.user:
      self.log(LogType.INFO, f"REACTION/REMOVE/{self._getMessagePath(message)}" , f"{user.name}({user.id}) : {self._getEmoji(reaction.emoji)} -> {self._getMessageContent(message)}")

  @staticmethod
  def _getEmoji(emoji : discord.Emoji) -> str:
    return emoji if isinstance(emoji, str) else f":{emoji.name}:"

  ###############
  #    MEMBER   #
  ###############
  @commands.Cog.listener()
  async def on_member_join(self, member : discord.Member):
    self.log(LogType.QUESTION, f"USER/JOIN" , f"{member.name}({member.id})")


  async def on_member_remove(self, member : discord.Member):
    self.log(LogType.QUESTION, f"USER/REMOVE" , f"{member.name}({member.id})")



def setup(bot):
  bot.add_cog(Track(bot))