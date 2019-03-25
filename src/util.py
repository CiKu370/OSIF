import os, csv
from progress.bar import Bar as ProgressBar

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(ROOT_DIR, 'output/photos')
OUTPUT_CSVS_DIR = os.path.join(ROOT_DIR, 'output/csv')

def write_directory(path):
  try:
    os.makedirs(path)
  except FileExistsError as ex:
    pass
def delete_file(path):
  os.remove(path)

def join_path(a, b):
  return os.path.join(a,b)

def relative_path(absolute_path):
  return absolute_path.replace(ROOT_DIR, "")[1:]

def write_photo(file_name, data):
  photo = None
  photo_path = '%s/%s' % (relative_path(PHOTOS_DIR), file_name)
  with open(photo_path, 'wb') as photo:
    photo.write(data)
    photo.close()
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

def save_list_of_dicts(file_name: str, l: list, fields: list):
  with open(file_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    progress_bar = ProgressBar('Saving %s' % relative_path(file_name), max=len(l))
    for el in l:
      row = {}
      for field in fields:
        try:
          row[field] = el[field]
        except KeyError as ex:
          raise ex
      if row.keys():
        writer.writerow(row)
      progress_bar.next()
    f.close()
  print()
  return f