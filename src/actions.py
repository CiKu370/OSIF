import os
from definitions import terminal, user_request_exit
from src.api import Facebook

fbApiInstance = Facebook()


def token(terminal):
  fbApiInstance.login()
  fbApiInstance.access_token()
  fbApiInstance.write_access_token()

def clear(terminal):
  os.system('cls' if os.name=='nt' else 'clear')

def exit_action(terminal):
  clear(terminal)
  exit()
