from osc_gen import sig
from osc_gen import wavetable
from osc_gen import visualize
from uuid import uuid4
import os_utils
import os


def render_directory():
    return os.path.join(os.getcwd(), 'renders')


def create_render_directory():
    os_utils.create_directory_if_not_exist(render_directory())


def visualize_wavetable(wavetable, directory='', filename='', save=False):
    if save:
        if not len(directory) > 0: raise "Missing directory parameter"
        if not len(filename) > 0: raise "Missing filename parameter"

        filepath = os.path.join(directory, filename)

        visualize.plot_wavetable(wavetable, save=filepath)
    else:
        visualize.plot_wavetable(wavetable)


def load_wavetable(filepath, samples=2048, tables=2, resynthesize=False):
    signal_generator = sig.SigGen(num_points=samples)
    return wavetable.WaveTable(tables).from_wav(filepath, sig_gen=signal_generator, resynthesize=resynthesize)


def save_wavetable(filepath, wavetable):
    wavetable.to_wav(filepath)


def process_wavetable(
    wavetable: wavetable.WaveTable
):
    if not wavetable: raise "Wavetable must be given, process failed."

    root_folder = os.path.join(".\\wavetables", os_utils.create_timestamp()) # TODO: What to do with folder limit???

    os_utils.create_directory_if_not_exist(root_folder)
    wavetable_filename, graph_filename = generate_wavetable_filename()

    visualize_wavetable(wavetable, root_folder, filename=graph_filename, save=True)
    save_wavetable(os.path.join(root_folder, wavetable_filename), wavetable)
    

def generate_wavetable_filename():
    unique_filename = os_utils.generate_unique_filename()
    return (unique_filename + ".wav", unique_filename + ".png")