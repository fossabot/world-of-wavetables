import wave
from osc_gen import sig
from osc_gen import wavetable
from osc_gen import visualize
from uuid import uuid4
import os_utils
import os
import numpy as np


def render_directory():
    return os.path.join(os.getcwd(), 'renders')


def create_render_directory():
    os_utils.create_directory_if_not_exist(render_directory())


def visualize_wavetable(wavetable, save=True):
    if save:
        filename = 'temp_' + str(uuid4()) + '.png'
        filepath = os.path.join(render_directory(), filename)

        visualize.plot_wavetable(wavetable, save=filepath)
        os_utils.sha256_hash_file(filepath, filename)
    else:
        visualize.plot_wavetable(wavetable)


def load_wavetable(filepath, samples=2048, tables=2, resynthesize=False):
    signalGenerator = sig.SigGen(num_points=samples)
    return wavetable.WaveTable(tables).from_wav(filepath, sig_gen=signalGenerator, resynthesize=resynthesize)


def save_wavetable(filepath, wavetable):
    wavetable.to_wav(filepath)


def process_wavetable(
    wavetable: wavetable.WaveTable,
    export_filepath: str,
    visualize: bool = True
):
    if visualize and wavetable is not None: visualize_wavetable(wavetable)
    if export_filepath is not None: save_wavetable(export_filepath, wavetable)


def morph_two_wavetables(wavetable_A: wavetable.WaveTable, wavetable_B: wavetable.WaveTable, times_cycle=32):
    visualize_wavetable(wavetable_A, save=False)
    visualize_wavetable(wavetable_B, save=False)

    return wavetable.WaveTable(times_cycle, 
        waves=sig.morph((
            wavetable_A.get_wave_at_index(0),
            wavetable_B.get_wave_at_index(0)
        ), times_cycle)
    )


def morph_wavetable_to_zero(
    target_wavetable: wavetable.WaveTable, 
    times_cycle=32
):
    zero_wavetable = wavetable.WaveTable(1, waves=[np.zeros(target_wavetable.wave_len)])

    visualize_wavetable(target_wavetable, save=False)
    visualize_wavetable(zero_wavetable, save=False)

    return wavetable.WaveTable(times_cycle, 
        waves=sig.morph((
            target_wavetable.get_wave_at_index(0),
            zero_wavetable.get_wave_at_index(0)
        ), times_cycle)
    )