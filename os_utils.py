import os
import hashlib
import uuid

def uuid_identifier():
    return str(uuid.uuid4())


def generate_unique_filename(filetype = ".wav"):
    return uuid_identifier() + filetype


"""
    Replace filename in filepath with a sha256.
    Example: filepath../test/item.wav | filename..item.wav -> /test/<sha256>.wav
"""
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


def does_folder_exist(filepath):
    return os.path.exists(filepath)


def create_directory_if_not_exist(filepath):
    if not does_folder_exist(filepath=filepath):
        os.mkdir(filepath)