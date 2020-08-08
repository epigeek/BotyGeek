from typing import List
from .Collumn import Collumn

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
