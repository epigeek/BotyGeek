from enum import IntEnum

class LogType(IntEnum):
  INFO =     0
  QUESTION = 1
  WARNING =  2
  ERROR =    3
  VALIDATE = 4

LogColor = {
  LogType.INFO:     0x2F92F6,
  LogType.QUESTION: 0xAB55D3,
  LogType.WARNING:  0xF6A72F,
  LogType.ERROR:    0xF85E49,
  LogType.VALIDATE: 0x97D82E
}

LogConsoleColor = {
  LogType.INFO:     34,
  LogType.QUESTION: 35,
  LogType.WARNING:  33,
  LogType.ERROR:    31,
  LogType.VALIDATE: 32
}

LogTitle = {
  LogType.INFO:     "Information",
  LogType.QUESTION: "Question",
  LogType.WARNING:  "Warning",
  LogType.ERROR:    "Error",
  LogType.VALIDATE: "Validate"
}

LogIcon = {
  LogType.INFO:     "https://cdn.discordapp.com/attachments/603629644503056400/717072436281213059/Information.png",
  LogType.QUESTION: "https://cdn.discordapp.com/attachments/603629644503056400/717149682521866310/Question.png",
  LogType.WARNING:  "https://cdn.discordapp.com/attachments/603629644503056400/717073534945591296/Warning.png",
  LogType.ERROR:    "https://cdn.discordapp.com/attachments/603629644503056400/717141827198910504/Error.png",
  LogType.VALIDATE: "https://cdn.discordapp.com/attachments/603629644503056400/717149882179387402/Validate.png"
}
