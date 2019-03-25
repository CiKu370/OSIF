import os, csv
from definitions import terminal, user_request_exit, OUTPUT_CSVS_DIR
from src.api import Facebook, BASE_URL as fb_base_url
from src.util import write_directory, relative_path

fbApiInstance = Facebook()

def token(terminal):
  fbApiInstance.login()
  fbApiInstance.write_access_token()

def clear(terminal):
  os.system('cls' if os.name=='nt' else 'clear')

def about(terminal):
  clear(terminal)
  terminal.logo()
  terminal.about()

def exit_action(terminal):
  clear(terminal)
  exit()

def fetch_friends(terminal):
  terminal.write('-'* 44)
  try:
    friends = fbApiInstance.get_friends()
    with open('%s/friends.csv' % OUTPUT_CSVS_DIR, 'w') as f:
      fieldnames = ['id', 'name', 'picture']
      writer = csv.DictWriter(f, fieldnames=fieldnames, )
      writer.writeheader()
      for friend in friends:
        picture = fbApiInstance.get_profile_picture(friend['id'])
        row = { 'id': friend['id'], 'name': friend['name'], 'picture': picture.name }
        terminal.write([row['id'], row['name']])
        writer.writerow(row)
      f.close()
    terminal.write('%s friends found' % len(friends))
  except IOError as ex:
    terminal.warning('Token not generated')
    terminal.info('Eject "token" command to get it.')

