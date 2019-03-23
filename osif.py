from definitions import define_directories
from src.api import Facebook
from src.messages import Message

define_directories()

fbApiInstance = Facebook()

fbApiInstance.login()
fbApiInstance.access_token()
fbApiInstance.write_access_token()