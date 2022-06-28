import typing
import librosa
import numpy as np
import soundfile
import os
import math

import typer
from . import string_utils
from . import os_utils

def get_zero_crossings(samples: np.ndarray):
    zero_crossings = librosa.zero_crossings(samples)
    zero_crossing_indexes = np.nonzero(zero_crossings)
    if len(zero_crossing_indexes) > 1: raise "Please convert your sample to mono."

    zero_crossing_indexes_array = zero_crossing_indexes[0]
        
    if zero_crossing_indexes_array.size % 2 != 0:
        zero_crossing_indexes_array = zero_crossing_indexes_array[:zero_crossing_indexes_array.size - 1]

    return zero_crossing_indexes_array

"""
    Calculates a percentage [default: .005] of len(zero_crossings) to split on.
"""
def calculate_magic_modulo_at_index(index: int, zero_crossings: np.array, split_level_percentage=.005):
    if zero_crossings.size == 0: raise "No zero crossing found and array is empty."
    
    magic_split = int(zero_crossings.size * split_level_percentage)

    if magic_split < 1: raise "Magic cannot work on sample due to small sample size."

    return zero_crossings[index] % magic_split == 0

"""
    Get zero_crossings from sample.
    Split by index using magic function
    Where split is true append
    Return simple zero crossing indexes
"""
def find_zero_crossings_at_magic_modulo(sample: np.ndarray):
    zero_crossings = get_zero_crossings(sample)

    split_indexes = np.empty((zero_crossings.size))
    for n in range(zero_crossings.size):
        split_indexes[n] = calculate_magic_modulo_at_index(n, zero_crossings=zero_crossings)

    result_zero_crossing_indexes = []
    for i in range(split_indexes.size):
        if split_indexes[i] == True:
            result_zero_crossing_indexes.append(zero_crossings[i])

    return np.array(result_zero_crossing_indexes)


"""
    This should split into n'th samples but where n'th is below total zero_crossings.
"""
def find_zero_crossings(samples: np.ndarray, split_count):
    zero_crossings = get_zero_crossings(samples)
    
    if not zero_crossings.any() or len(zero_crossings) <= 0: raise "Provided samples are empty or have no zero crossings."
    if split_count > len(zero_crossings): raise "Zero crossings must be above split count."

    split_at = math.trunc(len(zero_crossings) / split_count)

    chunks = []
    for split_times in range(split_count):
        chunks.append(zero_crossings[split_at * split_times:split_at * (split_times + 1)])

    return np.array(chunks)


def load_wavefile(filepath: str, sr=44100, mono = False) -> typing.Tuple[np.ndarray, int]:
    return librosa.load(filepath, sr=sr, mono=mono)


"""
    Get crossing with magic split and iterate over each two columns until no left.
"""
def split_wavefile_into_microsamples_magic(samples: np.ndarray) -> typing.List:
    crossings = find_zero_crossings_at_magic_modulo(samples)

    micro_samples = []
    for n in range(crossings.size - 1):
        micro_sample = samples[crossings[n]:crossings[n+1]]
        micro_samples.append(list(micro_sample))

    return np.array(micro_samples)


def split_wavefile_into_microsamples(samples: np.ndarray, split) -> typing.List:
    crossings: np.ndarray = find_zero_crossings(samples, split)

    micro_samples = np.empty((0, crossings.shape[1]))
    for crossing in crossings:
        micro_sample = np.array(samples[crossing], ndmin=2)
        micro_samples = np.append(micro_samples, micro_sample, axis=0)

    return micro_samples


def write_microsamples(
    list_of_microsamples: np.array, 
    relative_folder_path: str,
    samplerate=44100
):
    if not relative_folder_path: raise "Missing relative_folder_path."

    root_folder: str = ".\\microsamples"

    os_utils.create_directory_if_not_exist(root_folder)

    directory = os.path.join(root_folder, string_utils.strip_symbols_from_path_name(relative_folder_path))

    if not list_of_microsamples.any(): raise "List of microsamples empty or no samples provided."
    if os_utils.does_folder_exist(directory): raise "Folder exists, please set a new name."

    with typer.progressbar(list_of_microsamples) as progress:
        for micro_sample in progress:
            index = str(progress.pos + 1)
            filepath = os.path.join(directory, index + "-" + os_utils.generate_unique_filename() + '.wav')

            os_utils.create_directory_if_not_exist(directory)

            soundfile.write(
                filepath,
                micro_sample,
                samplerate=samplerate
            )

            typer.echo("- created microsample with index [" + index + "]")


def sample_info(filepath: str):
    samples, samplerate = load_wavefile(filepath, mono = False)

    result = {
        "data": samples, 
        "samplerate": samplerate, 
        "length": samples.size,
        "dimensions": samples.shape
    }

    return result