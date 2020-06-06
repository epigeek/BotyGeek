import discord
from discord.ext.commands import Bot
from botygeek.logs import ServerLogs, LogType
from botygeek.config.Config import Config



class BotyGeek(Bot):

  initial_extensions = [
    'botygeek.commands.track',
    'botygeek.commands.staff'
  ]

  def __init__(self, command_prefix : str, configPath : str):
    self.config = Config(configPath)
    super().__init__(command_prefix)
    self.logs = ServerLogs.ServerLogs("run/logs")
    for extension in self.initial_extensions:
      self.load_extension(extension)  

  def run(self, *args : list, **kwargs):
    lst = list(args)
    if len(lst) < 1:
      lst.append(self.config.token)
      args = tuple(lst)
    keys = kwargs.keys()
    if not "bot" in keys:
      kwargs["bot"] = True
    if not "reconnect" in keys:
      kwargs['reconnect'] = True
    return super().run(*args, **kwargs)(self)