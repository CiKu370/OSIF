# -*- coding: utf-8 -*-
import sys, getpass, readline
from enum import Enum


LOGO_WIDTH = 46

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
  def about(self):
    self.write( '''
                    %sINFORMATION%s
 ------------------------------------------------------

    Author     Debby Anggraini 'CiKu370'
    Name       OSIF 'Open Source Information Facebook'
    CodeName   D3b2y
    version    full version
    Date       16/05/2018 09:35:12
    Team       Blackhole Security
    Email      xnver404@gmail.com
    Telegram   @CiKu370

* if you find any errors or problems , please contact
  author
'''%(Terminal.Color.GREEN,Terminal.Color.WHITE))
  
  def message(self, text, message_type = None):
    if (not message_type):
      message_type = self.message_type
    return '{0}{1}'.format(self.color(message_type), text)
  
  def set_message_type(self, message_type):
    self.message_type = message_type
  
  def awaiting_for_command_message(self):
    return '%sosif %s>> ' % (Terminal.Color.RED, Terminal.Color.WHITE)
  
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