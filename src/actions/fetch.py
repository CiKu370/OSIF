import csv
from progress.bar import Bar as ProgressBar
from definitions import OUTPUT_CSVS_DIR
from src.actions import facebook_api
from src.util import save_list_of_dicts

def token_not_generated(terminal, ex):
  terminal.error(str(ex))
  terminal.warning('Token has not been generated')
  terminal.info('Eject "token" command to get it.')

def fetch_friends(terminal):
  terminal.write('-'* 44)
  friends = []
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  save_list_of_dicts('%s/friends.csv' % OUTPUT_CSVS_DIR, friends, ['id', 'name'])
  terminal.info('%s friends found' % len(friends))

def fetch_photos(terminal):
  terminal.write('-'* 44)
  friends = []
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  progress_bar = ProgressBar('Saving friends photos', max=len(friends))
  for friend in friends:
    picture = facebook_api.get_profile_picture(friend['id'])
    friend['picture'] = picture
    progress_bar.next()
  save_list_of_dicts('%s/friends.csv' % OUTPUT_CSVS_DIR, friends, ['id', 'name', 'picture'])
  terminal.info('%s friends found' % len(friends))

def fetch_ids(terminal):
  terminal.write('-'* 44)
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  save_list_of_dicts('%s/friend_ids.csv' % OUTPUT_CSVS_DIR, friends, ['id'])
  terminal.info('%s friends found' % len(friends))

def fetch_phones(terminal):
  terminal.write('-'* 44)
  phones = []
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  progress_bar = ProgressBar('Fetching phones', max=len(friends))
  for friend in friends:
    friend_data = facebook_api.get_profile_data(friend['id'])
    friend['phone'] = friend_data.get('mobile_phone', None)
    phones.append(friend['phone'])
    progress_bar.next()
  save_list_of_dicts('%s/friend_phones.csv' % OUTPUT_CSVS_DIR, friends, ['id', 'name', 'phone'])
  terminal.info('%s/%s phones found' % (len(friends), len(phones)))

def fetch_emails(terminal):
  terminal.write('-'* 44)
  emails = []
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  progress_bar = ProgressBar('Fetching emails', max=len(friends))
  for friend in friends:
    friend_data = facebook_api.get_profile_data(friend['id'])
    friend['email'] = friend_data.get('email', None)
    emails.append(friend['email'])
    progress_bar.next()
  save_list_of_dicts('%s/friend_emails.csv' % OUTPUT_CSVS_DIR, friends, ['id', 'name', 'email'])
  terminal.info('%s/%s emails found' % (len(friends), len(emails)))

def fetch_all(terminal):
  terminal.write('-'* 44)
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  progress_bar = ProgressBar('Fetching basic data', max=len(friends))
  for friend in friends:
    friend_data = facebook_api.get_profile_data(friend['id'])
    picture = facebook_api.get_profile_picture(friend['id'])
    friend['picture'] = picture.name
    friend['phone'] = friend_data.get('mobile_phone', None)
    friend['email'] = friend_data.get('email', None)
    friend['username'] = friend_data.get('username', None)
    progress_bar.next()
  file_name = '%s/friend_all.csv' % OUTPUT_CSVS_DIR
  fields = ['id', 'username', 'name', 'email', 'phone', 'picture']
  save_list_of_dicts(file_name, friends, fields)
  terminal.info('%s friends found' % len(friends))