import os
import hashlib

def sha256_hash_file(filepath, filename):
    BLOCK_SIZE = pow(2, 16)

    file_hash = hashlib.sha256()
    with open(filepath, 'rb') as file:
        bytes = file.read(BLOCK_SIZE)
        while len(bytes) > 0:
            file_hash.update(bytes)
            bytes = file.read(BLOCK_SIZE)

    target_filepath = filepath.replace(filename, file_hash.hexdigest() + "." + filename.split(".")[1])
    rename_file(filepath, target_filepath)

def rename_file(filepath, new_filepath):
    if os.path.exists(new_filepath): 
        os.remove(new_filepath)
    os.rename(filepath, new_filepath)

def create_directory_if_not_exist(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)