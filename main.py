from uuid import uuid4
from osc_gen import wavetable
from osc_gen import sig
from osc_gen import visualize
import soundfile as sf
import numpy as np
import librosa
import librosa.display
import hashlib
import os
import typer


app = typer.Typer()
# sg = sig.SigGen(num_points=2048)
# wt = wavetable.WaveTable(32).from_wav('./samples/sample.wav', sig_gen=sg, resynthesize=False)
# visualize.plot_wavetable(wt, save='./samples/sample_1_result.png')
# wt.to_wav('./samples/sample_1_result.wav');

# wt2 = wavetable.WaveTable(16)
# wt2.waves = sig.morph(wt.waves, 128);
# wt2.to_wav('./samples/sample_1_result_morph.wav');

file, samplerate = librosa.load("./samples/sample.wav")
librosa.display.waveshow(file, sr=samplerate)

def find_zero_crossings(samples, split_level_percentage=.005):
    zero_crossings = librosa.zero_crossings(file)
    zero_crossing_indexes = np.nonzero(zero_crossings)
    zero_crossing_indexes_array = zero_crossing_indexes[0] 
    
    if zero_crossing_indexes_array.size % 2 != 0: 
        zero_crossing_indexes_array = zero_crossing_indexes_array[:zero_crossing_indexes_array.size - 1]

    print((zero_crossing_indexes_array.size * split_level_percentage))

    split_indexes = np.array([zero_crossing_indexes_array[n] % int(zero_crossing_indexes_array.size * split_level_percentage) == 0 for n in range(zero_crossing_indexes_array.size)])
    
    zero_crossing_result = []
    for i in range(split_indexes.size):
        if split_indexes[i] == True:
            zero_crossing_result.append(zero_crossing_indexes_array[i])

    return np.array(zero_crossing_result)

def split_file_at(samples):
    splits = []
    crossings = find_zero_crossings(samples)
    for n in range(crossings.size - 1):
        splits.append(samples[crossings[n]:crossings[n+1]])

    return splits

def write_splits(splits):
    i = 0
    for split in splits:
        sf.write("./samples/splits/sample_" + str(i) + ".wav", split, samplerate=44100)
        i += 1

splits = split_file_at(file)
write_splits(splits)

def visualize_wavetable(wavetable):
    path = './renders/'
    filename = 'temp_' + str(uuid4()) + '.png'
    filepath = os.path.join(path, filename)

    visualize.plot_wavetable(wavetable, save=filepath)
    sha256_hash_file(filepath, filename)

def sha256_hash_file(filepath, filename):
    BLOCK_SIZE = pow(2, 16)

    file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(filepath, 'rb') as f: # Open the file to read it's bytes
        bytes = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(bytes) > 0: # While there is still data being read from the file
            file_hash.update(bytes) # Update the hash
            bytes = f.read(BLOCK_SIZE) # Read the next block from the file

    target_filepath = filepath.replace(filename, file_hash.hexdigest() + "." + filename.split(".")[1])
    rename_file(filepath, target_filepath)

def rename_file(filepath, new_filepath):
    if os.path.exists(new_filepath): 
        os.remove(new_filepath)
    os.rename(filepath, new_filepath)

def load_wavetable(filepath, samples=2048, tables=2, resynthesize=False):
    signalGenerator = sig.SigGen(num_points=samples)
    return wavetable.WaveTable(tables).from_wav(filepath, sig_gen=signalGenerator, resynthesize=resynthesize)

def save_wavetable(filepath, wavetable):
    wavetable.to_wav(filepath)

@app.command()
def version():
    typer.echo("[World of Wavetables | Backend | v0.1 | David Dembinski]")

@app.command()
def process_wavetable(import_filepath = typer.Argument(None), export_filepath = typer.Argument(None), visualize_wavetable: bool = True):
    """
        Imports a .wav file from a folder.
        Splits it into slices by using zero crossings and picking .005% of total sampled zero crossings.
        Afterwards generates an wavetable image and process its contents to generate an unique SHA256 name.
        After all is done save the wavetable.
    """
    wavetable = None
    if import_filepath is not None: wavetable = load_wavetable(import_filepath)
    if visualize_wavetable == True and wavetable is not None: visualize_wavetable(wavetable)
    if export_filepath is not None: save_wavetable(export_filepath, wavetable)

if __name__ == '__main__':
    typer.echo("Use --help for more information.")
    app()