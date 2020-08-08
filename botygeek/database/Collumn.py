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
