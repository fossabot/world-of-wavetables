import typer
from . import sampling_app
from . import wavetable_app

# Initalize Typer
app = typer.Typer()
app.add_typer(sampling_app.app, name="sampling")
app.add_typer(wavetable_app.app, name="wavetable")


# Global commands
@app.command()
def version():
    version_text = "[World of Wavetables | Backend | v0.1 | Inflamously]"
    typer.echo(version_text)
    return version_text


if __name__ == '__main__':
    app()