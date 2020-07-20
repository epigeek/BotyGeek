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
    self.name = self.__typeCheck(name, str)
    self.thetype = self.__typeCheck(thetype, type)
    self.primaryKey = self.__typeCheck(primaryKey, bool)
    self.notNull = self.__typeCheck(notNull, bool)
    self.unique = self.__typeCheck(unique, bool)
    self.default = self.__typeCheck(default, thetype, True)
    if not primaryKey and autoIncremental:
      raise ValueError(f"collumn {self.name} can be autoIncremental only if is primaryKey")
    self.autoIncremental = self.__typeCheck(autoIncremental, bool)

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
  def __typeCheck(variable : any, thetype : type, canBeNone : bool = False) -> any:
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

class Table:
  name : str
  collumns : List[Collumn]

  def __init__(self, name : str, collumns : List[Collumn]):
    self.name = self.__typeCheck(name, str)
    self.collumns = self.__typeCheck(collumns, list)
    i = 0
    for collumn in collumns:
      if not isinstance(collumn, Collumn):
        raise TypeError(f"`collumns` index {i} expected `Collumn` type, get : {collumn.__class__.__name__}")
      i += 1


  def check(self, cursor : sqlite3.Cursor):
    cursor.execute(f"PRAGMA table_info ({self.name});") # FIXME Unsave need to be sterize
    tableDatabase = set([collumn[1:] for collumn in cursor.fetchall()])
    tablePrototype = set([collumn.toTurple() for collumn in self.collumns])
    return tableDatabase == tablePrototype

  def create(self, cursor :sqlite3.Cursor):
    # FIXME Unsave need to be sterize
    sql = f"CREATE TABLE IF NOT EXISTS `{self.name}` (" + ", ".join([collumn.toSQL() for collumn in self.collumns]) + ");"
    cursor.execute(sql)

  @staticmethod
  def __typeCheck(variable : any, thetype : type, canBeNone : bool = False) -> any:
    if not (canBeNone and variable == None) and not isinstance(variable, thetype):
      raise TypeError(f"`{(variable)}` expected `{thetype.__name__}` type, get : {variable.__class__.__name__}") # TODO add variable name
    return variable




class Database:

  connection : sqlite3.Connection
  tables : List[Table]

  def __init__(self, path : str, tables : List[Table]):
    self.connection = sqlite3.connect(self.__typeCheck(path, str))
    self.tables = self.__typeCheck(tables, list)
    i = 0
    for table in tables:
      if not isinstance(table, Table):
        raise TypeError(f"`tables` index {i} expected `Table` type, get : {table.__class__.__name__}")
      self.addTable(table)
      i += 1


  def addTable(self, table : Table):
    self.__action(self.__typeCheck(table, Table).create)
    self.__action(table.check)

  def __del__(self):
    self.connection.close()

  def __action(self, action):
    cursor = self.getCursor()
    callReturn = action(cursor)
    self.connection.commit()
    return callReturn

  def getCursor(self):
    return self.connection.cursor()

  @staticmethod
  def __typeCheck(variable : any, thetype : type, canBeNone : bool = False) -> any:
    if not (canBeNone and variable == None) and not isinstance(variable, thetype):
      raise TypeError(f"`{(variable)}` expected `{thetype.__name__}` type, get : {variable.__class__.__name__}") # TODO add variable name
    return variable

