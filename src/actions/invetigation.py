from src.terminal import Terminal
from src.actions import facebook_api

def find_friends_of(terminal: Terminal, params: dict = {}):
  profile_id = params.get('profile-id', None)
  if(not profile_id):
    terminal.error('No profile id provided')
    terminal.info('Try again using -profile-id=<profile id>')
    return
  else:
    print(profile_id)
    friends = facebook_api.get_friends_of(profile_id)

def genderify_photos(terminal):
  pass

def find_friends_of_depth(terminal):
  pass