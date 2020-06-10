from yaml import safe_load
import os



class Config:

  token : str
  logs : str

  def __init__(self, path : str):
    self._path = path
    self.reload()

  def reload(self):
    with open(self._path, "r") as file:
      config = safe_load(file.read())
    self.checkConfig(config)
    self._import(config)

  @staticmethod
  def checkConfig(config : any):
    if not isinstance(config, dict):
      raise TypeError("config: checkConfig: `config` expected `dict` type, get : " + type(config))
    Config._safeTypeCheck(config, "token", str)
    Config._safeTypeCheck(config, "logs", str)
    Config._safeTypeCheck(config, "roleOnJoin", list)
    for i in config["roleOnJoin"]:
      if not isinstance(i, int):
        raise TypeError("config: checkConfig: a `roleOnJoin` expected `int` type, get : " + type(i))
    logs = config["logs"]
    if not os.path.exists(logs):
      os.mkdir(logs)
    elif not os.path.isdir(logs):
      raise FileExistsError(f'logs is not a directory : "{logs}"')


  @staticmethod
  def _safeTypeCheck(config : dict, key : str, thetype : any):
    if not key in config.keys():
      raise TypeError(f"config: checkConfig: no `{key}` property")
    value = config[key]
    if not isinstance(value, thetype):
      raise TypeError(f"config: checkConfig: `{key}` expected `{thetype.__name__}` type, get : {value.__class__.__name__}")

  def _import(self, config : dict):
    self.token = config["token"]
    self.logs = config["logs"]
    self.roleOnJoin = config["roleOnJoin"]
