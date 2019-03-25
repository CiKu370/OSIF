# -*- coding: utf-8 -*-
import sys, getpass, readline
from enum import Enum

LOGO_ASCII = open('src/assets/logo.txt', 'r').read()
LOGO_WIDTH = 60

ABOUT_INFORMATION = open('src/assets/about.txt', 'r').read()

def separate_params(param):
  param = str(param)
  key_value = param.split('=')
  key = str(key_value[0]).replace('-', '', 1)
  try:
    value = str(key_value[1]).strip()
  except IndexError:
    value = None
  return (key, value)

class CommandNotFoundException(Exception):
  def __init__(self, command_key):
    msg = 'Command "%s" not found' % command_key
    super(CommandNotFoundException, self).__init__(msg)
class Terminal:

  def __init__(self, *args, **kwargs):
    self.message_type = Terminal.MessageType.LOG
  
  def write(self, message, message_type = None):
    print(self.message(message, message_type))
  
  def error(self, message):
    self.write('[x] %s' % message, Terminal.MessageType.ERROR)

  def info(self, message):
    self.write('[i] %s' % message, Terminal.MessageType.INFO)

  def warning(self, message):
    self.write('[w] %s' % message, Terminal.MessageType.WARNING)

  def success(self, message):
    self.write('[✔] %s' % message, Terminal.MessageType.SUCCESS)

  def read(self, **kwargs):
    message = kwargs.get('message')
    message_type = kwargs.get('message_type')
    hide_input = kwargs.get('hide_input')
    message_text = self.message(message, message_type)
    if (hide_input):
      raw = getpass.getpass(message_text)
    else:
      try:
        raw = raw_input(message_text)
      except NameError:
        raw = input(message_text)
    return '{0}'.format(raw).strip()
  
  def clean(self, showLogo = False):
    if(showLogo):
      self.logo()
  
  def logo(self, message = None, message_type = None):
    print(Terminal.Color.BCYAN)
    for line in LOGO_ASCII.split('\n'):
      print(str(line).center(LOGO_WIDTH - len(line)))
    print(Terminal.Color.COLOR_OFF)
    if (message):
      # TODO: center the message
      message_to_print = '{0}[{3}{1}{2}]'.format(Terminal.Color.WHITE, message, Terminal.Color.WHITE, Terminal.Color.CYAN)
      print(message_to_print.center(LOGO_WIDTH))
    print()
  def about(self):
    for line in ABOUT_INFORMATION.split('\n'):
      print(str(line).ljust(LOGO_WIDTH))
  
  def message(self, text, message_type = None):
    if (not message_type):
      message_type = self.message_type
    return '{0}{1}'.format(self.color(message_type), text)
  
  def set_message_type(self, message_type):
    self.message_type = message_type
  
  def awaiting_for_command_message(self):
    return '%sOSSI %s>> ' % (Terminal.Color.BICYAN, Terminal.Color.WHITE)
  
  def run_command(self, navegation_menu):
    while True:
      command_raw = self.read_command()
      command_instruction = command_raw.split(" ")[0]
      if(command_instruction):
        break
    params = None
    if(self.command_has_params(command_raw)):
      params = dict(map(separate_params, command_raw.split(' ')[1:]))
    try:
      navegation_menu.run_command(command_instruction, params, self)
    except CommandNotFoundException as ex:
      self.error(str(ex))

  def read_command(self):
    awaiting_message = self.awaiting_for_command_message()
    return self.read(message = awaiting_message, message_type = Terminal.MessageType.LOG).strip()
  
  def command_has_params(self, command):
    return len(str(command).split(' ')) > 1


  def color(self, message_type):
    color = ''
    if(message_type == Terminal.MessageType.ERROR):
      color = Terminal.Color.RED
    elif(message_type == Terminal.MessageType.INFO):
      color = Terminal.Color.CYAN
    elif(message_type == Terminal.MessageType.WARNING):
      color = Terminal.Color.YELLOW
    elif(message_type == Terminal.MessageType.SUCCESS):
      color = Terminal.Color.GREEN
    elif(message_type == Terminal.MessageType.LOG):
      color = Terminal.Color.WHITE
    return color

  class MessageType(Enum):
    SUCCESS = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    LOG = 4
  class Color:# Reset
    COLOR_OFF="\033[0m"       # Text Reset

    # Regular Colors
    BLACK="\033[0;30m"        # Black
    RED="\033[0;31m"          # Red
    GREEN="\033[0;32m"        # Green
    YELLOW="\033[0;33m"       # Yellow
    BLUE="\033[0;34m"         # Blue
    PURPLE="\033[0;35m"       # Purple
    CYAN="\033[0;36m"         # Cyan
    WHITE="\033[0;37m"        # White

    # Bold
    BBLACK="\033[1;30m"       # Black
    BRED="\033[1;31m"         # Red
    BGREEN="\033[1;32m"       # Green
    BYELLOW="\033[1;33m"      # Yellow
    BBLUE="\033[1;34m"        # Blue
    BPURPLE="\033[1;35m"      # Purple
    BCYAN="\033[1;36m"        # Cyan
    BWHITE="\033[1;37m"       # White

    # Underline
    UBLACK="\033[4;30m"       # Black
    URED="\033[4;31m"         # Red
    UGREEN="\033[4;32m"       # Green
    UYELLOW="\033[4;33m"      # Yellow
    UBLUE="\033[4;34m"        # Blue
    UPURPLE="\033[4;35m"      # Purple
    UCYAN="\033[4;36m"        # Cyan
    UWHITE="\033[4;37m"       # White

    # Background
    ON_BLACK="\033[40m"       # Black
    ON_RED="\033[41m"         # Red
    ON_GREEN="\033[42m"       # Green
    ON_YELLOW="\033[43m"      # Yellow
    ON_BLUE="\033[44m"        # Blue
    ON_PURPLE="\033[45m"      # Purple
    ON_CYAN="\033[46m"        # Cyan
    ON_WHITE="\033[47m"       # White

    # High Intensty
    IBLACK="\033[0;90m"       # Black
    IRED="\033[0;91m"         # Red
    IGREEN="\033[0;92m"       # Green
    IYELLOW="\033[0;93m"      # Yellow
    IBLUE="\033[0;94m"        # Blue
    IPURPLE="\033[0;95m"      # Purple
    ICYAN="\033[0;96m"        # Cyan
    IWHITE="\033[0;97m"       # White

    # Bold High Intensty
    BIBLACK="\033[1;90m"      # Black
    BIRED="\033[1;91m"        # Red
    BIGREEN="\033[1;92m"      # Green
    BIYELLOW="\033[1;93m"     # Yellow
    BIBLUE="\033[1;94m"       # Blue
    BIPURPLE="\033[1;95m"     # Purple
    BICYAN="\033[1;96m"       # Cyan
    BIWHITE="\033[1;97m"      # White

    # High Intensty backgrounds
    ON_IBLACK="\033[0;100m"   # Black
    ON_IRED="\033[0;101m"     # Red
    ON_IGREEN="\033[0;102m"   # Green
    ON_IYELLOW="\033[0;103m"  # Yellow
    ON_IBLUE="\033[0;104m"    # Blue
    ON_IPURPLE="\033[10;95m"  # Purple
    ON_ICYAN="\033[0;106m"    # Cyan
    ON_IWHITE="\033[0;107m"   # White

if not sys.platform in ["linux","linux2"]:
  Terminal.Color.WHITE = ''
  Terminal.Color.GREEN = ''
  Terminal.Color.RED = ''