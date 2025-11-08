import sys
import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_undo(app):
    @app.command()
    def undo():
        command: str = " ".join(sys.argv[1:])
        try:
            console_service.undo()
        except Exception as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
