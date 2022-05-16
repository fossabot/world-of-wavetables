import typing
import wave
import typer
import signal_manipulation
import signal_showcase
import wavetable_utils
import wavetable_morphing
import sampling_app

# Initalize Typer
app = typer.Typer()
app.add_typer(sampling_app.app, name="sampling")

# Global commands
@app.command()
def version():
    typer.echo("[World of Wavetables | Backend | v0.1 | David Dembinski]")

@app.command()
def showcase_wavefile(import_filepath: str):
    samples, samplerate = signal_manipulation.load_wavefile(import_filepath)
    signal_showcase.visualize_signal(samples)

@app.command()
def process_sample_to_wavetable(
    import_filepath = typer.Argument(None),
    export_directory = typer.Argument(None),
    visualize_wavetable: bool = True
):
    """
        Process given sample (.wav) to wavetable.
        Splits it into slices by using zero crossings and picking .005% of total sampled zero crossings.
        Afterwards generates an wavetable image and process its contents to generate an unique SHA256 name.
        After all is done save the wavetable.
    """
    if not import_filepath: return
    if not export_directory: return

    wavetable = wavetable_utils.load_wavetable(import_filepath)
    if not wavetable: return

    wavetable_utils.process_wavetable(
        wavetable, 
        export_directory=export_directory, 
        visualize_wavetable=visualize_wavetable
    )


@app.command()
def interpolate_n_wavetables(
    visualize_wavetable: bool,
    wavetable_paths: typing.List[str],
):
    if not wavetable_paths or len(wavetable_paths) <= 0: return
    print(len(wavetable_paths),wavetable_paths)

    typer.echo("- Loading wavetables")

    wavetables = list(map(lambda path: wavetable_utils.load_wavetable(path, tables=1), wavetable_paths))
    print(wavetables)
    if not wavetables or len(wavetables) <= 0: raise "Loading of wavetables failed"

    if visualize_wavetable:
        for wavetable in wavetables:
            typer.echo("- Visualizing wavetable")
            wavetable_utils.visualize_wavetable(wavetable=wavetable)

    typer.echo("- Morphing wavetables")
    morphed_wavetable = wavetable_morphing.morph_n_wavetables(wavetables=wavetables, times_cycle=32)

    typer.echo("- Processing morphed wavetable")
    if morphed_wavetable: 
        wavetable_utils.process_wavetable(morphed_wavetable)


@app.command()
def interpolate_two_wavetables(
    wavetable_a_filepath: str, 
    wavetable_b_filepath: str,
    visualize_wavetable = typer.Argument(False)
):
    if not wavetable_a_filepath: return
    if not wavetable_b_filepath: return

    typer.echo("- Loading wavetable")

    wavetable_A, wavetable_B = \
        wavetable_utils.load_wavetable(wavetable_a_filepath, tables=1), \
        wavetable_utils.load_wavetable(wavetable_b_filepath, tables=1)

    if visualize_wavetable:
        typer.echo("- Visualizing wavetable A")
        wavetable_utils.visualize_wavetable(wavetable_A)

        typer.echo("- Visualizing wavetable B")
        wavetable_utils.visualize_wavetable(wavetable_B)

    typer.echo("- Morphing wavetable A -> B")
    morphed_wavetable = wavetable_morphing.morph_two_wavetables(
        wavetable_A=wavetable_A,
        wavetable_B=wavetable_B
    )

    typer.echo("- Processing morphed wavetable")
    if morphed_wavetable: 
        wavetable_utils.process_wavetable(morphed_wavetable)


@app.command()
def interpolate_wavetable_to_zero(
    wavetable_filepath: str, 
    export_filepath: str,
    visualize_wavetable = typer.Argument(True)
):
    if not wavetable_filepath: return
    wavetable = wavetable_utils.load_wavetable(wavetable_filepath, tables=1)

    morphed_wavetable = wavetable_morphing.morph_wavetable_to_zero(target_wavetable=wavetable)
    if morphed_wavetable:
        wavetable_utils.process_wavetable(
            morphed_wavetable,
            export_filepath=export_filepath,
            visualize=visualize_wavetable
        )


@app.command()
def interpolate_euclidean_wavetable():
    typer.echo("Needs to be implemented.")

if __name__ == '__main__':
    app()