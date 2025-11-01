from src.common.config import LOGGING_CONFIG

import sys
from pathlib import Path

import typer
from typer_shell import make_typer_shell
from typer import Context

from src.dependencies.container import Container
from src.enums.archive_format import ArchiveFormat
from src.enums.file_mode import FileReadMode
from src.services.init_services import init_services


console_service = init_services()

app = make_typer_shell(prompt="$~ ")

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
    command:str = "ls"
    if long_form:
        command += " -l"
    if all_files:
        command += " -a"
    for path in paths:
        command += f" {path}"
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

@app.command()
def cat(
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
    command: str = "cat"
    if mode: command += " -b"
    command += f" {Path}"
    try:
        mode = FileReadMode.bytes if mode else FileReadMode.string
        data = console_service.cat(
            filename,
            mode=mode,
        )
        if isinstance(data, bytes):
            sys.stdout.buffer.write(data)
        else:
            sys.stdout.write(data)
    except OSError as e:
        typer.echo(e)
    console_service._history.append_command_to_history(command)

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
    if recursive: command += " -r"
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
    command = f"mv {source} {dest}"
    try:
        
        console_service.mv(source, dest)
    except OSError as e:
        typer.echo(e)
    except PermissionError as e:
        typer.echo(e)
    console_service._history.append_command_to_history(command)

@app.command()
def rm(
    recursive: bool = typer.Option(False, "-r", "--recursive", help="remove directories and their contents recursively"),
    paths: list[Path] = typer.Argument(..., )
) -> None:
    command: str = "rm"
    if recursive: command += f" -r"
    for path in paths:
        command += f" {path}"
        try:
            console_service.rm(
                                        recursive,
                                        path
            )
        except OSError as e:
           typer.echo(e)
    console_service._history.append_command_to_history(command)

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

@app.command()
def zip(
    folder: Path = typer.Argument(...),
    archive_name: Path = typer.Argument(...)
) -> None:
    command: str = f"zip {folder} {archive_name}"
    try:
        
        console_service.pack(folder, archive_name, ArchiveFormat.zipfile)
    except OSError as e:
        typer.echo(e)
    console_service._history.append_command_to_history(command)

@app.command()
def unzip(
    archive: Path = typer.Argument(...),
    dest: Path = typer.Argument(default=Path("."))
) -> None:
    command: str = f"unzip {archive} {dest}"
    try:
        console_service.unpack(archive, dest, ArchiveFormat.zipfile)
    except OSError as e:
        typer.echo(e)
    console_service._history.append_command_to_history(command)

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
    command = "grep"
    if recursive: command += " -r"
    if ignorecase: command += " -i"
    command += f" {pattern}"
    for file in files: command += f" {file}"
    try:
        contents = console_service.grep(recursive, ignorecase, pattern, files)
        sys.stdout.writelines(contents)
    except Exception as e:
        typer.echo(e)
    console_service._history.append_command_to_history(command)

@app.command()
def history(ctx: Context):
    try:
        command_history: list[str] = console_service.history()
        sys.stdout.writelines(command_history)
    except Exception as e:
        typer.echo(e)
    console_service._history.append_command_to_history("history")

if __name__ == "__main__":
    app()
