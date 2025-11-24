from pathlib import Path

import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_rm(app):
    @app.command()
    def rm(
        recursive: bool = typer.Option(False, "-r", "--recursive", help="remove directories and their contents recursively"),
        paths: list[Path] = typer.Argument(..., )
    ) -> None:
        """
        Remove the file(s)
        """
        command: str = "rm"
        if recursive:
            command += " -r"
        for path in paths:
            command += f" {path}"
            try:
                console_service.rm(
                                            recursive,
                                            path
                )
            except OSError as e:
               typer.echo(e)
            except PermissionError as e:
                typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
