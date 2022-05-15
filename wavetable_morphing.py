from osc_gen import wavetable
from osc_gen import sig
import wavetable_utils

def morph_two_wavetables(wavetable_A: wavetable.WaveTable, wavetable_B: wavetable.WaveTable, times_cycle=32):
    wavetable_utils.visualize_wavetable(wavetable_A, save=False)
    wavetable_utils.visualize_wavetable(wavetable_B, save=False)

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

    wavetable_utils.visualize_wavetable(target_wavetable, save=False)
    wavetable_utils.visualize_wavetable(zero_wavetable, save=False)

    return wavetable.WaveTable(times_cycle, 
        waves=sig.morph((
            target_wavetable.get_wave_at_index(0),
            zero_wavetable.get_wave_at_index(0)
        ), times_cycle)
    )