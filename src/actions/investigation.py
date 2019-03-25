import os
from facebook import GraphAPIError
from src.terminal import Terminal
from src.util import write_directory, save_list_of_dicts
from definitions import OUTPUT_CSVS_FRIENDS_DIR
from src.actions import facebook_api

def find_friends_of(terminal: Terminal, params: dict):
  profile_id = params.get('id', None)
  if not profile_id:
    terminal.error('No profile id provided')
    terminal.info('Try again using -profile-id=<profile id>')
    return
  else:
    terminal.info('Getting friends of %s' % profile_id)
    try:
      friends_of = facebook_api.get_friends_of(profile_id)
      if len(friends_of) > 0:
        friend_directory = '%s/%s' % (OUTPUT_CSVS_FRIENDS_DIR, profile_id)
        file_name = '%s/friends.csv' % friend_directory
        try:
          os.mkdir(friend_directory)
        except FileExistsError:
          pass
        save_list_of_dicts(file_name, friends_of, ['id', 'name'])
    except GraphAPIError as ex:
      terminal.error(str(ex))

def find_friends_of_my_friends(terminal: Terminal):
  terminal.info('Getting friends of all')
  friends = facebook_api.get_friends()
  for friend in friends:
    find_friends_of(terminal, {'id': friend['id']})

def genderify_photos(terminal):
  pass

def find_friends_of_depth(terminal):
  pass