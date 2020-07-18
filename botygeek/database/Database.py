import sqlite3
from typing import List
# from varname import nameof


class Collumn:
  name : str
  thetype : object
  primaryKey : bool
  autoIncremental : bool
  notNull : bool
  unique : bool
  default: any

  typeName = {
    int: "INTEGER",
    bool: "BOOL",
    str: "TEXT"
  }

  convertToSQL = {
    bool : lambda value: '0' if not value else '1'
  }
  toPython = {
    bool : lambda value: value == '1'
  }

  def __init__(self, name : str, thetype : type, *, primaryKey : bool = False, autoIncremental : bool = False, notNull : bool = False, unique : bool = False, default : any = None):
    self.name = self._TypeCheck(name, str)
    self.thetype = self._TypeCheck(thetype, type)
    self.primaryKey = self._TypeCheck(primaryKey, bool)
    self.notNull = self._TypeCheck(notNull, bool)
    self.unique = self._TypeCheck(unique, bool)
    self.default = self._TypeCheck(default, thetype, True)
    if not primaryKey and autoIncremental:
      raise ValueError(f"collumn {self.name} can be autoIncremental only if is primaryKey")
    self.autoIncremental = self._TypeCheck(autoIncremental, bool)

  def toTurple(self):
    return (
      self.name,
      self.typeName[self.thetype] if self.thetype in self.typeName else self.typeName.__name__,
      self.boolToSQL(self.notNull),
      self.convertToSQL[self.thetype](self.default) if self.thetype in self.convertToSQL else self.default,
      self.boolToSQL(self.primaryKey)
    )

  def toSQL(self):
    sql = f"{self.name} {self.typeName[self.thetype]} "
    if self.primaryKey:
      sql += "PRIMARY KEY "
    if self.autoIncremental:
      sql += "AUTOINCREMENT "
    if self.notNull:
      sql += "NOT NULL "
    if self.unique:
      sql += "UNIQUE "
    if self.default != None:
      sql += f"DEFAULT {self.convertToSQL[self.thetype](self.default) if self.thetype in self.convertToSQL else self.default}"
    return sql

  @staticmethod
  def boolToSQL(value):
    return 0 if not value else 1

  @staticmethod
  def _TypeCheck(variable : any, thetype : type, canBeNone : bool = False) -> any:
    if not (canBeNone and variable == None) and not isinstance(variable, thetype):
      raise TypeError(f"`{(variable)}` expected `{thetype.__name__}` type, get : {variable.__class__.__name__}") # TODO add variable name
    return variable

  def __eq__(self, value):
    if isinstance(value, tuple) and len(value) == 6:
      return \
        value[1] == self.name and \
        value[2] == self.thetype.__name__ and \
        value[3] == self.notNull and \
        value[4] == self.default and \
        value[5] == self.primaryKey
    if isinstance(value, Collumn):
      return \
        self.name == value.name and \
        self.thetype == value.thetype and \
        self.notNull == value.notNull and \
        self.default == value.default and \
        self.unique == value.unique and \
        self.primaryKey == value.primaryKey and \
        self.autoIncremental == value.autoIncremental
    return super().__eq__(value)




class Database:

  PERMISSIONGROUP_TABLE : List[Collumn] = [
    Collumn("id", int, primaryKey=True, notNull=True, autoIncremental=True), # `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    Collumn("admin_ping", bool, notNull=True, default=False), # `admin_ping` BOOL NOT NULL DEFAULT 0,
    Collumn("admin_clear", bool, notNull=True, default=False), # `admin_clear` BOOL NOT NULL DEFAULT 0,
    Collumn("role_addRole", bool, notNull=True, default=False), # `role_addRole` BOOL NOT NULL DEFAULT 0,
    Collumn("role_removeRole", bool, notNull=True, default=False) # `role_removeRole` BOOL NOT NULL DEFAULT 0
  ]

  WARN_TABLE : List[Collumn] = [
    Collumn("id", int, primaryKey=True, notNull=True, autoIncremental=True), # `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    Collumn("accuser_uid", int, notNull=True), # `admin_ping` BOOL NOT NULL DEFAULT 0,
    Collumn("accused_uid", int, notNull=True), # `admin_clear` BOOL NOT NULL DEFAULT 0,
    Collumn("reason", str, notNull=True), # `role_addRole` BOOL NOT NULL DEFAULT 0,
    Collumn("proof", str) # `role_removeRole` BOOL NOT NULL DEFAULT 0
  ]

  connection : sqlite3.Connection

  def __init__(self, path : str):
    self.connection = sqlite3.connect(path)

    a = self.__safeLoad()
    print(a)

  def __del__(self):
    self.connection.close()

  def __safeLoad(self):
    self.__CreateTable("permissionGroup", self.PERMISSIONGROUP_TABLE)
    if not self.__ckeckTablePrototype("permissionGroup", self.PERMISSIONGROUP_TABLE):
      return False
    self.__CreateTable("warn", self.WARN_TABLE)
    if not self.__ckeckTablePrototype("warn", self.WARN_TABLE):
      return False
    return True

  def __action(self, action):
    cursor = self.__getCursor()
    callReturn = action(cursor)
    self.connection.commit()
    return callReturn

  def __ckeckTablePrototype(self, name : str, prototype : List[Collumn]):
    cursor = self.__getCursor()
    cursor.execute(f"PRAGMA table_info ({name});") # FIXME Unsave need to be sterize
    tableDatabase = set([collumn[1:] for collumn in cursor.fetchall()])
    tablePrototype = set([collumn.toTurple() for collumn in prototype])
    return tableDatabase == tablePrototype

  def __CreateTable(self, name : str, prototype : List[Collumn]):
    # FIXME Unsave need to be sterize
    sql = f"CREATE TABLE IF NOT EXISTS `{name}` (" + ", ".join([collumn.toSQL() for collumn in prototype]) + ");"
    def action(cursor : sqlite3.Cursor):
      cursor.execute(sql)
    cursor = self.__action(action)

  def __getCursor(self):
    return self.connection.cursor()


