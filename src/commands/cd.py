from pathlib import Path

import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_cd(app):
    @app.command()
    def cd(
        path: Path = typer.Argument(
            default=Path("~")
        )
    ) -> None:
        """
        Change the shell working directory
        """
        try:
            console_service.cd(path)
        except OSError as e:
            typer.echo(e)
        console_service._history.append_command_to_history(f"cd {path}")

    return app
