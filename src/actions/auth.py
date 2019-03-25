from src.actions import facebook_api

def token(terminal):
  facebook_api.login()
  facebook_api.write_access_token()