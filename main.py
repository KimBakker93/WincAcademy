__winc_id__ = 'ae539110d03e49ea8738fd413ac44ba8'
__human_name__ = 'files'
import os
from zipfile import ZipFile

def clean_cache():
    if os.path.exists('cache'):
        for filename in os.listdir('cache'):
            os.remove('cache/' + filename)
    else:
        os.mkdir('cache')

def cache_zip(zip_file_path: str, cache_dir_path: str):
    with ZipFile(zip_file_path, 'r') as zipObj:
         zipObj.extractall(cache_dir_path)

def cached_files():
    files = []
    for filename in os.listdir('cache'):
        if os.path.isfile('cache/' + filename):
            files.append(os.path.abspath('cache/' + filename))
    return files

def find_password(files: list):
    password = ''
    for file in files:
        with open(file) as f:
            content = f.read()
            lines = content.splitlines()
            for line in lines:
                if line.find('password') != -1:
                    password = line.replace('password: ', '')
    return password  

    
            
            

        



