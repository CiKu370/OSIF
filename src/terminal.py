import sys
from enum import Enum

LOGO_WIDTH = 44

class Terminal:
  class Color:
    WHITE = '\033[0m'
    GREEN = '\033[1;32m'
    RED = '\033[0;31m'
    BLUE = '\033[34;1m'
    YELLOW = '\033[93m'
    
  class MessageType(Enum):
    SUCCESS = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    LOG = 4

  def __init__(self, *args, **kwargs):
    self.message_type = Terminal.MessageType.LOG

  def set_message_type(self, message_type):
    self.message_type = message_type
  
  def print_logo(self, message = None, message_type = None):
    print(Terminal.Color.RED)
    print ('_     _'.center(LOGO_WIDTH))
    print ("o' \.=./ `o".center(LOGO_WIDTH))
    print ('(o o)'.center(LOGO_WIDTH))
    print ('ooO--(_)--Ooo'.center(LOGO_WIDTH))
    print (Terminal.Color.WHITE)
    print ('O S I F'.center(LOGO_WIDTH))
    if (message):
      terminal_message = self.message(message, Terminal.MessageType.SUCCESS)
      # TODO: center the message
      message_to_print = '{0}[{1}{2}]'.format(Terminal.Color.WHITE, terminal_message, Terminal.Color.WHITE)
      print(message_to_print.center(LOGO_WIDTH))

  def message(self, text, message_type = None):
    if (not message_type):
      message_type = self.message_type
    return '{0}{1}'.format(self.color(message_type), text)

  
  def write(self, message, message_type = None):
    print(self.message(message, message_type))

  def read(self, message, message_type = None):
    return raw_input(self.message(message, message_type))

  def color(self, message_type):
    color = ''
    if(message_type == Terminal.MessageType.ERROR):
      color = Terminal.Color.RED
    elif(message_type == Terminal.MessageType.INFO):
      color = Terminal.Color.BLUE
    elif(message_type == Terminal.MessageType.WARNING):
      color = Terminal.Color.YELLOW
    elif(message_type == Terminal.MessageType.SUCCESS):
      color = Terminal.Color.GREEN
    elif(message_type == Terminal.MessageType.LOG):
      color = Terminal.Color.WHITE
    return color


if not sys.platform in ["linux","linux2"]:
  Terminal.Color.WHITE = ''
  Terminal.Color.GREEN = ''
  Terminal.Color.RED = ''