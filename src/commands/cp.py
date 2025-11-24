from pathlib import Path

import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_cp(app):
    @app.command()
    def cp(
        recursive: bool = typer.Option(
            False, "-r", "--recursive", help="copy directories recursively"
        ),
        sources: list[Path] = typer.Argument(
            ...
        ),
        dest: Path = typer.Argument(
            ...
        )
    ) -> None:
        """
        Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.
        """
        command = "cp"
        if recursive:
            command += " -r"
        for source in sources:
            command += f" {source}"
            try:
                console_service.cp(
                                            recursive,
                                            source,
                                            dest
                )
            except OSError as e:
                typer.echo(e)
        command += f" {dest}"
        console_service._history.append_command_to_history(command)

    return app
