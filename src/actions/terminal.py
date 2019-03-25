import os

def clear(terminal):
  os.system('cls' if os.name=='nt' else 'clear')

def about(terminal):
  clear(terminal)
  terminal.logo()
  terminal.about()

def exit_action(terminal):
  clear(terminal)
  exit()