import typing
import librosa
from more_itertools import sample
import numpy as np
import soundfile as sf
import os

from os_utils import create_directory_if_not_exist

def find_zero_crossings(samples: np.ndarray, split_level_percentage=.005):
    zero_crossings = librosa.zero_crossings(samples)
    zero_crossing_indexes = np.nonzero(zero_crossings)
    if len(zero_crossing_indexes) > 1: raise "Please convert your sample to mono."

    zero_crossing_indexes_array = zero_crossing_indexes[0]
        
    if zero_crossing_indexes_array.size % 2 != 0:
        zero_crossing_indexes_array = zero_crossing_indexes_array[:zero_crossing_indexes_array.size - 1]

    split_indexes = np.array([zero_crossing_indexes_array[n] % int(zero_crossing_indexes_array.size * split_level_percentage) == 0 for n in range(zero_crossing_indexes_array.size)])
    
    result_zero_crossing_indexes = []
    for i in range(split_indexes.size):
        if split_indexes[i] == True:
            result_zero_crossing_indexes.append(zero_crossing_indexes_array[i])

    return np.array(result_zero_crossing_indexes)


def load_wavefile(filepath: str, mono = False) -> typing.Tuple[np.ndarray, int]:
    return librosa.load(filepath, mono=mono)


def split_wavefile_into_microsamples(samples: np.ndarray) -> typing.List:
    micro_samples = []
    crossings = find_zero_crossings(samples)

    for n in range(crossings.size - 1):
        micro_samples.append(samples[crossings[n]:crossings[n+1]])

    return micro_samples


def write_microsamples(
    list_of_microsamples, 
    directory_path: str,
    filename_prefix: str,
    samplerate=44100
):
    if not directory_path: return
    if not list_of_microsamples or not len(list_of_microsamples) > 0: return

    file_index = 0
    for micro_sample in list_of_microsamples:
        create_directory_if_not_exist(directory_path)
        sf.write(
            os.path.join(directory_path, filename_prefix + "_" + str(file_index) + ".wav"), 
            micro_sample,
            samplerate=samplerate
        )
        file_index += 1