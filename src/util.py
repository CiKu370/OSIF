import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(ROOT_DIR, 'output/photos')

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

def write_photo(file_name, data):
  photo = open('%s/%s' % (PHOTOS_DIR, file_name), 'w')
  photo.write(data)
  return photo

def to_dict(obj, classkey=None):
  if isinstance(obj, dict):
    data = {}
    for (k, v) in obj.items():
        data[k] = to_dict(v, classkey)
    return data
  elif hasattr(obj, "_ast"):
    return to_dict(obj._ast())
  elif hasattr(obj, "__iter__") and not isinstance(obj, str):
    return [to_dict(v, classkey) for v in obj]
  elif hasattr(obj, "__dict__"):
    data = dict([(key, to_dict(value, classkey)) 
        for key, value in obj.__dict__.items() 
        if not callable(value) and not key.startswith('_')])
    if classkey is not None and hasattr(obj, "__class__"):
        data[classkey] = obj.__class__.__name__
    return data
  else:
      return obj