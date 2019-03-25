from src.terminal import Terminal
from src.actions import facebook_api
from facebook import GraphAPIError

def find_friends_of(terminal: Terminal, params: dict = {}):
  profile_id = params.get('id', None)
  if not profile_id:
    terminal.error('No profile id provided')
    terminal.info('Try again using -profile-id=<profile id>')
    return
  else:
    try:
      friends = facebook_api.get_friends_of(profile_id)
      print(friends)
    except GraphAPIError as ex:
      terminal.error(str(ex))

def genderify_photos(terminal):
  pass

def find_friends_of_depth(terminal):
  pass