import typing
import typer
import wavetable_utils
import wavetable_morphing
import sample_manipulation
import sample_showcase

app = typer.Typer()


@app.command()
def interpolate_n_wavetables(
    visualize_wavetable: bool,
    wavetable_paths: typing.List[str],
):
    if not wavetable_paths or len(wavetable_paths) <= 0: return
    print(len(wavetable_paths),wavetable_paths)

    typer.echo("- Loading wavetables")

    wavetables = list(map(lambda path: wavetable_utils.load_wavetable(path, tables=1), wavetable_paths))
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
def showcase_wavefile(import_filepath: str):
    samples, samplerate = sample_manipulation.load_wavefile(import_filepath)
    sample_showcase.visualize_signal(samples)


@app.command()
def interpolate_euclidean_wavetable():
    typer.echo("Needs to be implemented.")