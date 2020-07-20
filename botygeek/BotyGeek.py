import discord
from discord.ext.commands import Bot
from botygeek.logs import ServerLogs, LogType
from botygeek.config.Config import Config
from botygeek.database import Database, Table, Collumn



class BotyGeek(Bot):

  config : Config
  logs : ServerLogs.ServerLogs
  database : Database

  initial_extensions = [
    'botygeek.commands.track',
    'botygeek.commands.staff',
    'botygeek.commands.roles'
  ]

  def __init__(self, command_prefix : str, configPath : str):
    self.config = Config(configPath)
    super().__init__(command_prefix)
    self.logs = ServerLogs.ServerLogs("run/logs")
    self.database = Database(self.config.database, [
      Table("permissionGroup", [
        Collumn("id", int, primaryKey=True, notNull=True, autoIncremental=True), # `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Collumn("admin_ping", bool, notNull=True, default=False), # `admin_ping` BOOL NOT NULL DEFAULT 0,
        Collumn("admin_clear", bool, notNull=True, default=False), # `admin_clear` BOOL NOT NULL DEFAULT 0,
        Collumn("role_addRole", bool, notNull=True, default=False), # `role_addRole` BOOL NOT NULL DEFAULT 0,
        Collumn("role_removeRole", bool, notNull=True, default=False) # `role_removeRole` BOOL NOT NULL DEFAULT 0
      ]),
      Table("warn", [
        Collumn("id", int, primaryKey=True, notNull=True, autoIncremental=True), # `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Collumn("accuser_uid", int, notNull=True), # `admin_ping` BOOL NOT NULL DEFAULT 0,
        Collumn("accused_uid", int, notNull=True), # `admin_clear` BOOL NOT NULL DEFAULT 0,
        Collumn("reason", str, notNull=True), # `role_addRole` BOOL NOT NULL DEFAULT 0,
        Collumn("proof", str) # `role_removeRole` BOOL NOT NULL DEFAULT 0
      ])
    ])
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