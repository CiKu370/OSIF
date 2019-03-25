from definitions import define_directories, terminal, user_request_exit
from src.navegation import navegation_menu

define_directories()

while (not user_request_exit):
  terminal.run_command(navegation_menu)