import discord
import asyncio
import typing

from botygeek.logs.LogType import LogType, LogColor, LogIcon, LogTitle

class ClientLogs():

  @staticmethod
  async def send(ctx, type : LogType, title : str, content : str = None) -> discord.Message:
    if not content:
      (content, title) = (title, content)
    embed : discord.Embed = discord.Embed(color=LogColor[type])
    embed.set_author(icon_url=LogIcon[type], name=title if title else LogTitle[type])
    embed.description = content
    return await ctx.send(embed=embed)

  @staticmethod
  async def question(
    client : discord.Client,
    ctx : discord.abc.Messageable,
    type : LogType,
    content : str,
    users : typing.List[discord.User],
    actions : typing.Dict[str, typing.Callable],
    deleteAfter : bool = False,
    timeout : float = None,
    onTimeOut : typing.Callable = None
  ) -> discord.Message:
    if isinstance(users, discord.User):
      users = [users]

    message : discord.Message = await ClientLogs.send(ctx, type, content)
    for emoji in actions:
      await message.add_reaction(emoji)

    def check(reaction : discord.Reaction, user : discord.User) -> bool:
      return reaction.message.id == message.id and user in users and str(reaction.emoji) in actions

    try:
      reaction, user = await client.wait_for('reaction_add', timeout=timeout, check=check)
    except asyncio.TimeoutError:
      if onTimeOut != None:
        await onTimeOut(message)
    else:
      action : callable = actions[str(reaction.emoji)]
      if callable(action):
        await action(message)
    if deleteAfter:
      await message.delete()
    return message

  @staticmethod
  async def validation(
    client : discord.Client,
    ctx : discord.abc.Messageable,
    message : str,
    user :discord.User,
    valid : callable,
    invalid : callable,
    deleteAfter : bool = True,
    timeout : float = None
  ):
    await ClientLogs.question(client, ctx, LogType.WARNING, message, [user], {"✔️": valid, "❌": invalid}, deleteAfter ,timeout, invalid)

  @staticmethod
  async def deletable(
    client : discord.Client,
    ctx : discord.abc.Messageable,
    type : LogType,
    message : str,
    user :discord.User,
    timeout : float = None
  ):
    await ClientLogs.question(client, ctx, type, message, [user], {"🗑️": None}, True ,timeout)


  @staticmethod
  async def helpMessage(ctx : discord.abc.Messageable, name : str, description : str, usage : str, arguments = None) -> discord.Message:
    embed : discord.Embed = discord.Embed(color=LogColor[LogType.INFO])
    embed.set_author(icon_url=LogIcon[LogType.INFO], name=str.capitalize(name))
    embed.description = description
    embed.add_field(name="Usage", value=f"`>{usage}`", inline=False)
    if arguments:
      embed.add_field(name="Arguments", value=str.join("\n - ", arguments), inline=False)
    return await ctx.send(embed=embed)