import sys

import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_history(app):
    @app.command()
    def history():
        """
        Display the history list
        """
        try:
            command_history: list[str] = console_service.history()
            sys.stdout.writelines(command_history)
        except Exception as e:
            typer.echo(e)
        console_service._history.append_command_to_history("history")

    return app
