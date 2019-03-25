import csv
from progress.bar import Bar as ProgressBar
from definitions import OUTPUT_CSVS_DIR
from src.actions import facebook_api

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
  with open('%s/friends.csv' % OUTPUT_CSVS_DIR, 'w') as f:
    fieldnames = ['id', 'name']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    progress_bar = ProgressBar('Fetching friends', max=len(friends))
    for friend in friends:
      row = { 'id': friend['id'], 'name': friend['name']}
      writer.writerow(row)
      progress_bar.next()
    f.close()
  print('')
  terminal.info('%s friends found' % len(friends))

def fetch_photos(terminal):
  terminal.write('-'* 44)
  friends = []
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  with open('%s/friends.csv' % OUTPUT_CSVS_DIR, 'w') as f:
    fieldnames = ['id', 'name', 'picture']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    progress_bar = ProgressBar('Fetching friends', max=len(friends))
    for friend in friends:
      picture = facebook_api.get_profile_picture(friend['id'])
      row = { 'id': friend['id'], 'name': friend['name'], 'picture': picture.name }
      writer.writerow(row)
      progress_bar.next()
    f.close()
  print('')
  terminal.info('%s friends found' % len(friends))

def fetch_ids(terminal):
  terminal.write('-'* 44)
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  with open('%s/friend_ids.csv' % OUTPUT_CSVS_DIR, 'w') as f:
    fieldnames = ['id']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    progress_bar = ProgressBar('Fetching ids', max=len(friends))
    for friend in friends:
      row = { 'id': friend['id']}
      writer.writerow(row)
      progress_bar.next()
    f.close()
  print('')
  terminal.info('%s friends found' % len(friends))

def fetch_phones(terminal):
  terminal.write('-'* 44)
  phones = []
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  with open('%s/friend_phones.csv' % OUTPUT_CSVS_DIR, 'w') as f:
    fieldnames = ['id', 'name', 'phone']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    progress_bar = ProgressBar('Fetching phones', max=len(friends))
    for friend in friends:
      friend_data = facebook_api.get_profile_data(friend['id'])
      try:
        phone = friend_data['mobile_phone']
      except KeyError:
        pass
      if(phone):
        phones.append(phone)
      row = { 'id': friend['id'], 'name': friend['name'], 'phone': phone }
      writer.writerow(row)
      progress_bar.next()
    f.close()
  print('')
  terminal.info('%s/%s phones found' % (len(friends), len(phones)))

def fetch_emails(terminal):
  terminal.write('-'* 44)
  mails = []
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  with open('%s/friend_mails.csv' % OUTPUT_CSVS_DIR, 'w') as f:
    fieldnames = ['id', 'name', 'email']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    progress_bar = ProgressBar('Fetching emails', max=len(friends))
    for friend in friends:
      friend_data = facebook_api.get_profile_data(friend['id'])
      try:
        email = friend_data['email']
      except KeyError:
        pass
      if(email):
        mails.append(email)
      row = { 'id': friend['id'], 'name': friend['name'], 'email': email }
      writer.writerow(row)
      progress_bar.next()
    f.close()
  print('')
  terminal.info('%s/%s mails found' % (len(friends), len(mails)))

def fetch_all(terminal):
  terminal.write('-'* 44)
  try:
    friends = facebook_api.get_friends()
  except IOError as ex:
    token_not_generated(terminal, ex)
  with open('%s/friend_all.csv' % OUTPUT_CSVS_DIR, 'w') as f:
    fieldnames = ['id', 'username', 'name', 'email', 'phone', 'picture']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    progress_bar = ProgressBar('Fetching basic informacion', max=len(friends))
    for friend in friends:
      friend_data = facebook_api.get_profile_data(friend['id'])
      picture = facebook_api.get_profile_picture(friend['id'])
      email = phone = username = None
      try:
        email = friend_data['email']
        phone = friend_data['mobile_phone']
        username = friend_data['username']
      except KeyError:
        pass
      row = { 
        'id': friend['id'],
        'username': username,
        'name': friend['name'],
        'phone': phone,
        'email': email,
        'picture': picture.name
      }
      writer.writerow(row)
      progress_bar.next()
    f.close()
  print('')
  terminal.info('%s friends found' % len(friends))