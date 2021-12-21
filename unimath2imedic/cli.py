import pathlib
import sys
import typing

import typer

from . import main as prog_main

app = typer.Typer()

@app.command()
def main(
    output_path: pathlib.Path = typer.Argument(
        ...,
        file_okay = True,
        dir_okay = False,
        allow_dash = True
    )
):
    stream: typing.Optional[typing.BinaryIO] = None

    try:
        if str(output_path) == "-":
            stream = sys.stdout.buffer
        else:
            stream = open(output_path, "bw")

        prog_main.generate(stream)
    finally:
        if stream:
            stream.close()
    