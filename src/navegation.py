from src.terminal import Terminal, CommandNotFoundException
from src.actions.auth import token
from src.actions.terminal import clear, about, exit_action
from src.actions.fetch import fetch_all, fetch_emails, fetch_friends, fetch_ids, fetch_phones, fetch_photos
from src.actions.investigation import find_friends_of, find_friends_of_my_friends
from definitions import terminal, user_request_exit

NAVEGATION_MENU_CONFIG = [
  {
    'title': 'Auth',
    'commands': [
      {'auth:facebook': ['Login in Facebook', token]},
    ]
  },
  {
    'title': 'Fetch Data',
    'commands': [
      {'fetch:friends': ['Fetch all id from friend list', fetch_friends, True]},
      {'fetch:ids': ['Fetch all id from friend list', fetch_ids, True]},
      {'fetch:phones': ['Fetch all phone number from friend list', fetch_phones, True]},
      {'fetch:emails': ['Fetch all emails from friend list', fetch_emails, True]},
      {'fetch:photos': ['Fetch all id from friend list', fetch_photos, True]},
      {'fetch:all': ['Fetch all emails from friend list', fetch_all, True]},
    ]
  },
  {
    'title': 'Investigation',
    'commands': [
      {'invest:friends-of': ['Fetch all id from friend list', find_friends_of, True]},
      {'invest:friends-of-all': ['Fetch all id from friend list', find_friends_of_my_friends, True]},
    ]
  },
  {
    'title': 'Bots',
    'commands': [
      {'bot': ['Open bot menu', None]}
    ]
  },
  {
    'title': 'Terminal',
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
    self.key = kwargs.get('key', '')
    self.action = kwargs.get('action', None)
    self.description = kwargs.get('decription','')
    self.stopable = False

class NavegationMenu:
  def __init__(self, *args, **kwargs):
    self.menu = kwargs.get('menu')
    self.commands = []

    for group in self.menu:
      for command in group['commands']:
        c = Command()
        c.key = list(command.keys())[0]
        c.description = command[c.key][0]
        c.action = command[c.key][1]
        try:
          c.stopable = command[c.key][2]
        except IndexError:
          pass
        self.commands.append(c)

  def command_keys(self):
    return map(lambda c: c.key, self.commands)

  def has_command(self, command_key):
    return any(map(lambda ck: ck == command_key, self.command_keys()))
  
  def find_command(self, command_key):
    found = list(filter(lambda ck: ck.key == command_key, self.commands))
    if(len(found) != 1):
      return None
    return found[0]
  
  def set_command(self, command_key, action):
    command = self.find_command(command_key)
    if(not command):
      command = Command(key=command_key, action=action)
      self.commands.append(command)
    else:
      command.action = action
  
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
        c.key = list(command.keys())[0]
        c.description = command[c.key][0]

        command_key = '  %s' % c.key
        command_description = '  %s' % c.description
        terminal.write(command_key.ljust(22) + command_description.ljust(22))

  def run_action(self, action, params, terminal):
    if(params):
      return action(terminal, params)
    else:
      return action(terminal)


  def run_command(self, command_key: str, params: dict, terminal: Terminal):
    if(not self.has_command(command_key)):
      raise CommandNotFoundException(command_key)
    command = self.find_command(command_key)
    if(command.action):
      if(not command.stopable):
        return self.run_action(command.action, params, terminal)
      try:
        self.run_action(command.action, params, terminal)
      except (KeyboardInterrupt, SystemExit):
        print('')
        terminal.info('Command stoped')
        


navegation_menu = NavegationMenu(menu=NAVEGATION_MENU_CONFIG)

def help_func(terminal):
  clear(terminal)
  terminal.logo()
  navegation_menu.display_menu(terminal)

help_action = lambda t: help_func(t)

navegation_menu.set_command('help', help_action)
navegation_menu.set_command('exit', exit_action) 
    