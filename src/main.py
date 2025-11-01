from src.common.config import LOGGING_CONFIG

import logging
import sys
from pathlib import Path

import typer
from typer_shell import make_typer_shell
from typer import Context

from src.dependencies.container import Container
from src.enums.file_mode import FileReadMode
from src.enums.archive_format import ArchiveFormat
from src.services.macos_console import LinuxConsoleService

app = typer.Typer()


def get_container(ctx: Context) -> Container:
    container = ctx.obj
    if not isinstance(container, Container):
        raise RuntimeError("DI container is not initialized")
    return container


@app.callback()
def main(ctx: Context):
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    ctx.obj = Container(
        console_service=LinuxConsoleService(logger=logger),
    )


@app.command()
def ls(
    ctx: Context,
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
    container: Container = get_container(ctx)
    for path in paths:
        try:
            content = container.console_service.ls(path, 
                                                all_files, 
                                                long_form
                                                )
            sys.stdout.write(f"{path}: \n")
            sys.stdout.writelines(content)
        except OSError as e:
            typer.echo(e)

@app.command()
def cd(
    ctx: Context,
    path: Path = typer.Argument(
        default=Path("~"), help=""
    )
) -> None:
    """
    Change the shell working directory
    """
    try:
        container: Container = get_container(ctx)
        container.console_service.cd(path)
    except OSError as e:
        typer.echo(e)

@app.command()
def cat(
    ctx: Context,
    filename: Path = typer.Argument(
        ..., exists=False, readable=False, help="File to print"
    ),
    mode: bool = typer.Option(
        False, "--bytes", "-b", help="Read as bytes"
    ),
) -> None:
    """
    Cat a file
    """
    try:
        container: Container = get_container(ctx)
        mode = FileReadMode.bytes if mode else FileReadMode.string
        data = container.console_service.cat(
            filename,
            mode=mode,
        )
        if isinstance(data, bytes):
            sys.stdout.buffer.write(data)
        else:
            sys.stdout.write(data)
    except OSError as e:
        typer.echo(e)

@app.command()
def cp(
    ctx: Context,
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
    container: Container = get_container(ctx)
    for source in sources:
        try:
            container.console_service.cp(
                                        recursive,
                                        source,
                                        dest
            )
        except OSError as e:
            typer.echo(e)

@app.command()
def mv(
    ctx: Context,
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
    try:
        container: Container = get_container()
        container.console_service.mv(source, dest)
    except OSError as e:
        typer.echo(e)
    except PermissionError as e:
        typer.echo(e)

@app.command()
def rm(
    ctx: Context,
    recursive: bool = typer.Option(False, "-r", "--recursive", help="remove directories and their contents recursively"),
    paths: list[Path] = typer.Argument(..., )
) -> None:
    container: Container = get_container(ctx)
    for path in paths:
        try:
            container.console_service.rm(
                                        recursive,
                                        path
            )
        except OSError as e:
           typer.echo(e)

@app.command()
def tar(
    ctx: Context,
    folder: Path = typer.Argument(...),
    archive_name: Path = typer.Argument(...)
) -> None:
    try:
        container: Container = get_container(ctx)
        container.console_service.pack(folder, archive_name, ArchiveFormat.gztar)
    except OSError as e:
        typer.echo(e)

@app.command()
def untar(
    ctx: Context,
    archive: Path = typer.Argument(...),
    dest: Path = typer.Argument(default=Path("."))
) -> None:
    try:
        container: Container = get_container(ctx)
        container.console_service.unpack(archive, dest, ArchiveFormat.gztar)
    except OSError as e:
        typer.echo(e)

@app.command()
def zip(
    ctx: Context,
    folder: Path = typer.Argument(...),
    archive_name: Path = typer.Argument(...)
) -> None:
    try:
        container: Container = get_container(ctx)
        container.console_service.pack(folder, archive_name, ArchiveFormat.zipfile)
    except OSError as e:
        typer.echo(e)

@app.command()
def unzip(
    ctx: Context,
    archive: Path = typer.Argument(...),
    dest: Path = typer.Argument(default=Path("."))
) -> None:
    try:
        container: Container = get_container(ctx)
        container.console_service.unpack(archive, dest, ArchiveFormat.zipfile)
    except OSError as e:
        typer.echo(e)

@app.command()
def grep(
    ctx: Context,
    recursive: bool = typer.Option(
        False, "-r", "--recursive", help="Recursively check child directories"
    ),
    ignorecase: bool = typer.Option(
        False, "-i", "-ignore-case", help="ignore case distinctions in patterns and data"
    ),
    pattern: str = typer.Argument(...),
    files: list[Path] = typer.Argument(default=Path("."))
) -> None:
    try:
        container: Container = get_container(ctx)
        contents = container.console_service.grep(recursive, ignorecase, pattern, files)
        sys.stdout.writelines(contents)
    except Exception as e:
        typer.echo(e)

if __name__ == "__main__":
    app()
