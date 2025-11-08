from pathlib import Path

import sys
import typer # type: ignore

from src.enums.archive_format import ArchiveFormat
from src.services.init_services import init_services

console_service = init_services()

def register_zip(app):
    @app.command()
    def zip(
        folder: Path = typer.Argument(...),
        archive_name: Path = typer.Argument(...)
    ) -> None:
        """
        Create archive .zip from file
        """
        command: str = " ".join(sys.argv[1:])
        try:
            console_service.pack(folder, archive_name, ArchiveFormat.zipfile)
        except OSError as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app

def register_unzip(app):
    @app.command()
    def unzip(
        archive: Path = typer.Argument(...),
        dest: Path = typer.Argument(default=Path("."))
    ) -> None:
        """
        Unarchive .zip archive
        """
        command: str = " ".join(sys.argv[1:])
        try:
            console_service.unpack(archive, dest, ArchiveFormat.zipfile)
        except OSError as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
