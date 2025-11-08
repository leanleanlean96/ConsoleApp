import sys
from pathlib import Path

import typer # type: ignore

from src.services.init_services import init_services

console_service = init_services()

def register_ls(app):
    @app.command()
    def ls(
        paths: list[Path] = typer.Argument(
            default=[Path(".")], allow_dash=True, help="directories to list contends of (default - current directory)"
        ),
        long_form: bool = typer.Option(
            False, "-l", "--long", help="use a long listing format"
        ),
        all_files: bool = typer.Option(
            False, "-a", "--all", help="do not ignore entries starting with ."
        )
    ) -> None:
        """
        List all files in a directory/directories.
        """
        command: str = " ".join(sys.argv[1:])
        for path in paths:
            try:
                content = console_service.ls(path,
                                                    all_files,
                                                    long_form
                                                    )
                sys.stdout.write(f"{path}: \n")
                sys.stdout.writelines(content)
            except OSError as e:
                typer.echo(e)
        console_service._history.append_command_to_history(command)

    return app
