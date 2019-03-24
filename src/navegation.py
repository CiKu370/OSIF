from src.terminal import Terminal, CommandNotFoundException
from src.actions import token, clear, exit_action, clear, fetch_friends, about
from definitions import terminal, user_request_exit

NAVEGATION_MENU_CONFIG = [
  {
    'title': '',
    'commands': [
      {'get:data': ['Fetch all friends data', None]},
      {'get:info': ['Show information about your friend', None]},
    ]
  },
  {
    'title': '',
    'commands': [
      {'fetch:friends': ['Fetch all id from friend list', fetch_friends]},
      {'fetch:ids': ['Fetch all id from friend list', None]},
      {'fetch:phones': ['Fetch all phone number from friend list', None]},
      {'fetch:mails': ['Fetch all emails from friend list', None]},
    ]
  },
  {
    'title': '',
    'commands': [
      {'token': ['Generate access token', token]},
      {'token:show': ['Show your access token', None]},
      {'token:rm': ['Show your access token', None]},
    ]
  },
  {
    'title': '',
    'commands': [
      {'bot': ['Open bot menu', None]}
    ]
  },
  {
    'title': '',
    'commands': [
      {'clear': ['Clear terminal', clear]},
      {'help': ['Show commands description', None]},
      {'about': ['Show information about this program', about]},
      {'exit': ['Exit the program', None]},
    ]  
  }
]

class Command:
  def __init__(self, *args, **kwargs):
    self.key = ''
    self.description = ''
    self.action = None


class NavegationMenu:
  def __init__(self, *args, **kwargs):
    self.menu = kwargs.get('menu')
    self.commands = []

    for group in self.menu:
      for command in group['commands']:
        c = Command()
        c.key = dict.keys(command)[0]
        c.description = command[c.key][0]
        c.action = command[c.key][1]
        self.commands.append(c)

  def command_keys(self):
    return map(lambda c: c.key, self.commands)
  def has_command(self, command_key):
    return any(map(lambda ck: ck == command_key, self.command_keys()))
  
  def find_command(self, command_key):
    found = filter(lambda ck: ck.key == command_key, self.commands)
    return found[0]
  
  def find_action(self, command_key):
    return self.find_command(command_key).action
  
  def display_menu(self, terminal):
    column_separator = ('-' * 18).center(22)
    terminal.write('Commands'.center(22) + 'Description'.center(22), Terminal.MessageType.SUCCESS)
    terminal.write(column_separator + column_separator, Terminal.MessageType.LOG)
    terminal.set_message_type(Terminal.MessageType.LOG)
    for i, group in enumerate(self.menu):
      if(i != 0):
        print('')
      for command in group['commands']:
        c = Command()
        c.key = dict.keys(command)[0]
        c.description = command[c.key][0]

        command_key = '  %s' % c.key
        command_description = '  %s' % c.description
        terminal.write(command_key.ljust(22) + command_description.ljust(22))

  def run_command(self, command_key, terminal):
    if(not self.has_command(command_key)):
      raise CommandNotFoundException(command_key)
    action = self.find_action(command_key)
    if(action):
      action(terminal)

navegation_menu = NavegationMenu(menu=NAVEGATION_MENU_CONFIG)

def help_func(terminal):
  clear()
  terminal.logo()
  navegation_menu.display_menu(terminal)

help_action = lambda t: help_func(t)

navegation_menu.find_command('help').action = help_action
navegation_menu.find_command('exit').action = exit_action
    