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


def visualize_wavetable(wavetable, directory, filename, save=False):
    if save:
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
    wavetable: wavetable.WaveTable,
    visualize: bool = True
):
    if not wavetable: raise "Wavetable must be given, process failed."

    root_folder = ".\wavetables" # TODO: What to do with folder limit???

    os_utils.create_directory_if_not_exist(root_folder)
    filename = os_utils.generate_unique_filename()

    visualize_wavetable(wavetable, root_folder, filename=filename, save=True)
    save_wavetable(os.path.join(root_folder, filename), wavetable)
    