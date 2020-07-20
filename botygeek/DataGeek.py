from .database import Database, Table, Collumn

class DataGeek(Database):
  def __init__(self, path : str):
    super().__init__(path, [
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
