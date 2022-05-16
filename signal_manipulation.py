from textwrap import indent
import typing
import librosa
from more_itertools import sample
import numpy as np
import soundfile
import os

import typer
import string_utils

from os_utils import create_directory_if_not_exist
import os_utils


def get_zero_crossings(samples: np.ndarray):
    zero_crossings = librosa.zero_crossings(samples)
    zero_crossing_indexes = np.nonzero(zero_crossings)
    if len(zero_crossing_indexes) > 1: raise "Please convert your sample to mono."

    zero_crossing_indexes_array = zero_crossing_indexes[0]
        
    if zero_crossing_indexes_array.size % 2 != 0:
        zero_crossing_indexes_array = zero_crossing_indexes_array[:zero_crossing_indexes_array.size - 1]

    return zero_crossing_indexes_array

def calculate_magic_modulo_at_index(index: int, zero_crossings: np.ndarray, split_level_percentage=.005):
    return zero_crossings[index] % int(zero_crossings.size * split_level_percentage) == 0

def find_zero_crossings_at_magic_modulo(samples: np.ndarray):
    zero_crossings = get_zero_crossings(samples)

    split_indexes = np.ndarray([])
    for n in range(zero_crossings.size):
        split_indexes = np.append(split_indexes, calculate_magic_modulo_at_index(n, zero_crossings=zero_crossings))

    result_zero_crossing_indexes = []
    for i in range(split_indexes.size):
        if split_indexes[i] == True:
            result_zero_crossing_indexes.append(zero_crossings[i])

    return np.array(result_zero_crossing_indexes)


"""
    This should split into n'th samples but where n'th is below total zero_crossings.
"""
def find_zero_crossings(samples: np.ndarray, splits = 4):
    zero_crossings = get_zero_crossings(samples)

    # split_indexes = np.ndarray([])
    # for n in range(zero_crossings.size):
    #     print(int(zero_crossings.size * split_level_percentage))
    #     if zero_crossings[n] % int(zero_crossings.size * split_level_percentage) == 0:
    #         split_indexes = np.append(split_indexes, zero_crossings[n])

    # result_zero_crossing_indexes = []
    # for i in range(split_indexes.size):
    #     if split_indexes[i] == True:
    #         result_zero_crossing_indexes.append(zero_crossings[i])

    return np.array([])


def load_wavefile(filepath: str, mono = False) -> typing.Tuple[np.ndarray, int]:
    return librosa.load(filepath, mono=mono)


def split_wavefile_into_microsamples_magic(samples: np.ndarray) -> typing.List:
    micro_samples = []
    crossings = find_zero_crossings_at_magic_modulo(samples)

    for n in range(crossings.size - 1):
        micro_samples.append(samples[crossings[n]:crossings[n+1]])

    return micro_samples


def split_wavefile_into_microsamples(samples: np.ndarray) -> typing.List:
    micro_samples = []
    crossings = find_zero_crossings(samples, 4)

    for n in range(crossings.size - 1):
        micro_samples.append(samples[crossings[n]:crossings[n+1]])

    return micro_samples


def write_microsamples(
    list_of_microsamples: typing.List, 
    relative_folder_path: str,
    samplerate=44100
):
    if not relative_folder_path: raise "Missing relative_folder_path."

    root_folder: str = ".\\microsamples"

    create_directory_if_not_exist(root_folder)

    directory = os.path.join(root_folder, string_utils.strip_symbols_from_path_name(relative_folder_path))

    if not list_of_microsamples or len(list_of_microsamples) <= 0: raise "Missing list of microsamples or empty."
    if os_utils.does_folder_exist(directory): raise "Folder exists, please set a new name."

    with typer.progressbar(list_of_microsamples) as progress:
        for micro_sample in progress:
            index = str(progress.pos + 1)
            filepath = os.path.join(directory, index + "-" + os_utils.generate_unique_filename())

            create_directory_if_not_exist(directory)

            soundfile.write(
                filepath,
                micro_sample,
                samplerate=samplerate
            )

            typer.echo("- created microsample with index [" + index + "]")