import typer
import signal_manipulation

app = typer.Typer()

@app.command()
def split_into_microsamples_magic(
    export_directory_path: str,
    import_filepath: str,
):
    """
       Split loaded sample into "micro-samples".
       Each "micro-sample" gets saved into a given directory.
    """
    samples, samplerate = signal_manipulation.load_wavefile(import_filepath, mono=True)
    if not samples.any(): raise "Failed to load wavefile."
    
    micro_samples = signal_manipulation.split_wavefile_into_microsamples_magic(samples)
    if not micro_samples: raise "Microsample split failed."

    signal_manipulation.write_microsamples(
        micro_samples, 
        export_directory_path,
        samplerate=samplerate
    )