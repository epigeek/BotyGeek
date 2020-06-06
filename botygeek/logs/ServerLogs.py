import datetime
from botygeek.logs.LogType import LogType, LogConsoleColor
import os
import io
from _datetime import timedelta



class ServerLogs():

  folder : str
  file : io.TextIOWrapper
  date : datetime.date

  def __init__(self, path : str):
    if not os.path.isdir(path):
      raise ValueError(f"no logs folder : {os.path.abspath(path)}")
    self.folder = path
    self.file = None
    self.date = datetime.date.today()
    self._createLogsFile()
    rows, columns = os.popen('stty size', 'r').read().split()
    print("DateTime                   │ Type     │ Action                                     │ Descrition")
    print(self._limitsize(int(columns), "───────────────────────────┼──────────┼────────────────────────────────────────────┼", "─"))

  def _createLogsFile(self):
    if self.file:
      self.file.close()
    self.file = open(os.path.join(self.folder, str(self.date) + ".log"), "a")

  def log(self, logType : LogType, action: str , content : str):
    print(
      "\x1b[90m" +
      datetime.datetime.now().isoformat() +
      f"\x1b[0m │ \x1b[{LogConsoleColor[logType]}m" +
      self._limitsize(8, f"{logType.name}") +
      "\x1b[0m │ " +
      self._limitsize(42, action) +
      "\x1b[0m │ \x1b[37m" +
      f"{content} "
    )
    self._write(f"[{datetime.datetime.now().isoformat()}] ({logType.name}) {{{action}}} {content}")
    
  @staticmethod
  def _limitsize(size : int, content : str, fill=" "):
    return content + fill * (size - len(content))

  def _write(self, content : str):
    today : date = datetime.date.today()
    if self.date != today:
      self._createLogsFile()
    if os.path.getsize(self.file.name):
      content = "\n" + content
    self.file.write(content)
    self._save()

  def _save(self):
    self.file.flush()
    os.fsync(self.file)

  def __del__(self):
    self.file.close()