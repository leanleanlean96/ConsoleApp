import sys
from pathlib import Path

import typer # type: ignore

from src.enums.file_mode import FileReadMode
from src.services.init_services import init_services

console_service = init_services()

def register_cat(app):
    @app.command()
    def cat(
        filename: Path = typer.Argument(
            ..., exists=False, readable=False, help="File to print"
        ),
        mode: bool = typer.Option(
            False, "--bytes", "-b", help="Read as bytes"
        ),
    ) -> None:
        """
        Cat a file
        """
        command: str = "cat"
        if mode:
            command += " -b"
        command += f" {Path}"
        try:
            readmode = FileReadMode.bytes if mode else FileReadMode.string
            data = console_service.cat(
                filename,
                mode=readmode,
            )
            if isinstance(data, bytes):
                sys.stdout.buffer.write(data)
            else:
                sys.stdout.write(data)
        except OSError as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
