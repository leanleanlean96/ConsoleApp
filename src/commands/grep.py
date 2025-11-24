import sys
from pathlib import Path

import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_grep(app):
    @app.command()
    def grep(
        recursive: bool = typer.Option(
            False, "-r", "--recursive", help="Recursively check child directories"
        ),
        ignorecase: bool = typer.Option(
            False, "-i", "-ignore-case", help="ignore case distinctions in patterns and data"
        ),
        pattern: str = typer.Argument(...),
        files: list[Path] = typer.Argument(default=Path("."))
    ) -> None:
        """
        Search for pattern in each file
        """
        command = "grep"
        if recursive:
            command += " -r"
        if ignorecase:
            command += " -i"
        command += f" {pattern}"
        for file in files:
            command += f" {file}"
        try:
            contents = console_service.grep(recursive, ignorecase, pattern, files)
            sys.stdout.writelines(contents)
        except Exception as e:
            typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
