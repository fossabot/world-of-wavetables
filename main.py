import typer
import signal_manipulation
import signal_showcase
import wavetable_utils

app = typer.Typer()

# file, samplerate = librosa.load("./samples/sample.wav")
# librosa.display.waveshow(file, sr=samplerate)
# splits = split_file_at(file)
# write_splits(splits)

@app.command()
def version():
    typer.echo("[World of Wavetables | Backend | v0.1 | David Dembinski]")

@app.command()
def showcase_wavefile(import_filepath: str):
    samples, samplerate = signal_manipulation.load_wavefile(import_filepath)
    signal_showcase.visualize_signal(samples)

@app.command()
def split_sample_to_micro_samples(
    export_directory_path: str,
    import_filepath: str,
    filename_prefix: str,
):
    """
        Loads up a given sample and splits it into "micro-samples".
        Each "micro-sample" gets saved into a given directory.
    """
    samples, samplerate = signal_manipulation.load_wavefile(import_filepath, mono=True)
    if not samples.any(): return
    
    micro_samples = signal_manipulation.split_wavefile_into_microsamples(samples)
    if not micro_samples: return

    print(micro_samples[0])

    signal_manipulation.write_microsamples(
        micro_samples, 
        export_directory_path, 
        filename_prefix=filename_prefix,
        samplerate=samplerate
    )

@app.command()
def process_sample(
    import_filepath = typer.Argument(None), 
    export_filepath = typer.Argument(None), 
    visualize_wavetable: bool = True
):
    """
        Imports a .wav file from a folder.
        Splits it into slices by using zero crossings and picking .005% of total sampled zero crossings.
        Afterwards generates an wavetable image and process its contents to generate an unique SHA256 name.
        After all is done save the wavetable.
    """
    wavetable = None
    if import_filepath is not None: wavetable = wavetable_utils.load_wavetable(import_filepath)
    if wavetable: wavetable_utils.process_wavetable(
        wavetable, 
        export_filepath=export_filepath, 
        visualize_wavetable=visualize_wavetable
    )


@app.command()
def interpolate_two_wavetables(
    wavetable_a_filepath: str, 
    wavetable_b_filepath: str,
    export_filepath: str,
    visualize_wavetable = typer.Argument(True)
):
    if not wavetable_a_filepath: return
    if not wavetable_b_filepath: return
    wavetable_A, wavetable_B = \
        wavetable_utils.load_wavetable(wavetable_a_filepath, tables=1), \
        wavetable_utils.load_wavetable(wavetable_b_filepath, tables=1)

    # wavetable_utils.visualize_wavetable(wavetable_A, save=False)
    # wavetable_utils.visualize_wavetable(wavetable_B, save=False)

    morphed_wavetable = wavetable_utils.morph_two_wavetables(wavetable_A=wavetable_A,wavetable_B=wavetable_B)
    if morphed_wavetable:
        wavetable_utils.process_wavetable(
            morphed_wavetable,
            export_filepath=export_filepath,
            visualize=visualize_wavetable
        )


@app.command()
def interpolate_wavetable_to_zero(
    wavetable_filepath: str, 
    export_filepath: str,
    visualize_wavetable = typer.Argument(True)
):
    if not wavetable_filepath: return
    wavetable = wavetable_utils.load_wavetable(wavetable_filepath, tables=1)

    morphed_wavetable = wavetable_utils.morph_wavetable_to_zero(target_wavetable=wavetable)
    if morphed_wavetable:
        wavetable_utils.process_wavetable(
            morphed_wavetable,
            export_filepath=export_filepath,
            visualize=visualize_wavetable
        )

if __name__ == '__main__':
    app()