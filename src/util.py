import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def write_directory(path):
  try:
    os.makedirs(path)
  except OSError:
    pass
def delete_file(path):
  os.remove(path)

def join_path(a, b):
  return os.path.join(a,b)

def relative_path(absolute_path):
  return absolute_path.replace(ROOT_DIR, "")