import sqlite3
from typing import List
from .Table import Table


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

