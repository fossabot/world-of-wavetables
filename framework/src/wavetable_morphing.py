import typing
from osc_gen import wavetable
from osc_gen import sig
import numpy as np
import wavetable_utils


def morph_n_wavetables(wavetables: typing.List[wavetable.WaveTable], times_cycle=32):
    if not wavetables or len(wavetables) <= 0: raise "No wavetables found"
    if len(wavetables) > times_cycle: raise "Too many wavetables, must be below times_cycle"

    signals = list(map(lambda wt: wt.get_wave_at_index(0), wavetables))

    return wavetable.WaveTable(
        times_cycle, 
        waves=sig.morph(tuple(signals), times_cycle)
    )


def morph_two_wavetables(wavetable_A: wavetable.WaveTable, wavetable_B: wavetable.WaveTable, times_cycle=32):
    return wavetable.WaveTable(
        times_cycle, 
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

    wavetable_utils.visualize_wavetable(target_wavetable, save=False)
    wavetable_utils.visualize_wavetable(zero_wavetable, save=False)

    return wavetable.WaveTable(times_cycle, 
        waves=sig.morph((
            target_wavetable.get_wave_at_index(0),
            zero_wavetable.get_wave_at_index(0)
        ), times_cycle)
    )