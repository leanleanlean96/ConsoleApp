from pathlib import Path

import typer # type: ignore

from src.enums.archive_format import ArchiveFormat
from src.services.init_services import init_services

console_service = init_services()

def register_tar(app):
    @app.command()
    def tar(
        folder: Path = typer.Argument(...),
        archive_name: Path = typer.Argument(...)
    ) -> None:
        command: str = f"tar {folder} {archive_name}"
        try:
            console_service.pack(folder, archive_name, ArchiveFormat.gztar)
        except OSError as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app

def register_untar(app):
    @app.command()
    def untar(
        archive: Path = typer.Argument(...),
        dest: Path = typer.Argument(default=Path("."))
    ) -> None:
        command: str = f"untar {archive} {dest}"
        try:

            console_service.unpack(archive, dest, ArchiveFormat.gztar)
        except OSError as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
