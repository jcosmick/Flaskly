import random
import string
import os
from config import ALLOWED_EXTENSIONS

def allowed_file(filename):
    d = filename.split('.',1)
    if len(d) == 2:
        return d[1] in ALLOWED_EXTENSIONS

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_file_path(path, fileName):
    return path+"/"+fileName

def delete_json_from_path(path):
    os.remove(path)