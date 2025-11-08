from pathlib import Path

import sys
import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_mv(app):
    @app.command()
    def mv(
        source: Path = typer.Argument(
            ...
        ),
        dest: Path = typer.Argument(
            ...
        )
    ) -> None:
        """
        Rename SOURCE to DEST, or move SOURCE to DIRECTORY
        """
        command: str = " ".join(sys.argv[1:])
        try:

            console_service.mv(source, dest)
        except OSError as e:
            typer.echo(e)
        except PermissionError as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
