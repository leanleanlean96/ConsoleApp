import logging
import os
import stat
import shutil
from datetime import datetime
from grp import getgrgid
from logging import Logger
from os import PathLike
from os import stat_result
from pwd import getpwuid
from pathlib import Path
from typing import Literal

from src.enums.file_mode import FileReadMode
from src.enums.archive_format import ArchiveFormat
from src.enums.archive_format import ExtensionName
from src.errors import WrongFormatError
from src.services.base import OSConsoleServiceBase


class LinuxConsoleService(OSConsoleServiceBase):
    def __init__(self, logger: Logger):
        self._logger = logger

    def ls(self,
            path: PathLike[str] | str,
            all_files: bool,
            long_form: bool
    ) -> list[str]:
        path = Path(path)
        if not path.exists():
            self._logger.error(f"Folder not found: {path}")
            raise FileNotFoundError(f"{path} does not exist")
        if not path.is_dir():
            self._logger.error(f"You entered {path} is not a directory")
            raise NotADirectoryError(f"{path} is not a directory")
        self._logger.info(f"Listing {path.absolute()}")
        directory_contents: list[str] = []
        for entry in path.iterdir():
            if not all_files and entry.name.startswith("."):
                continue
            if long_form:
                entry_info: stat_result = os.stat(entry.absolute())
                permissions: str = stat.filemode(entry_info.st_mode)
                nlinks: int = entry_info.st_nlink
                owner: str = getpwuid(entry_info.st_uid).pw_name
                group: str = getgrgid(entry_info.st_gid).gr_name
                size: int = entry_info.st_size
                mod_date: str = datetime.fromtimestamp(entry_info.st_mtime).strftime("%b %d %H:%M")
                directory_contents.append(f"{permissions} {nlinks} {owner} {group} {size} {mod_date} {entry.name}\n")
            else:
                directory_contents.append(entry.name + "\n")
        return directory_contents
    
    def cd(
        self,
        path: PathLike[str] | str
    ) -> None:
        path = Path(path)
        if not path.exists():
            self._logger.error(f"Folder not found: {path}")
            raise FileNotFoundError(path)
        if not path.is_dir():
            self._logger.error(f"You entered {path} is not a directory")
            raise NotADirectoryError(path)
        self._logger.info(f"Changing directory to {path}")
        os.chdir(path.absolute())

    def cp(
        self,
        recursive: bool,
        source: PathLike[str] | str,
        dest: PathLike[str] | str
    ) -> None:
        source = Path(source)
        dest = Path(dest)
        if not source.exists():
            self._logger.error(f"Folder not found: {dest}")
            raise FileNotFoundError(f"{source} does not exist")
        if source.is_dir() and dest.is_file():
            self._logger.error(f"Can't copy {source}[dir] to {dest}[file]")
            raise IsADirectoryError("")
        if source.is_dir() and not recursive:
            raise IsADirectoryError(f"Can't copy {source}, -r unspecified. Ommiting...")
        self._logger.info("Starting to copy...")
        if recursive and source.is_dir():
            shutil.copytree(source, dest)
        else:
            shutil.copy(source, dest)

    def cat(
        self,
        filename: PathLike[str] | str,
        mode: Literal[FileReadMode.string, FileReadMode.bytes] = FileReadMode.string,
    ) -> str | bytes:
        path: Path = Path(filename)
        if not path.exists(follow_symlinks=True):
            self._logger.error(f"File not found: {filename}")
            raise FileNotFoundError(filename)
        if path.is_dir(follow_symlinks=True):
            self._logger.error(f"You entered {filename} is not a file")
            raise IsADirectoryError(f"You entered {filename} is not a file")
        try:
            self._logger.info(f"Reading file {filename} in mode {mode}")
            match mode:
                case FileReadMode.string:
                    return path.read_text(encoding="utf-8")
                case FileReadMode.bytes:
                    return path.read_bytes()
        except OSError as e:
            self._logger.exception(f"Error reading {filename}: {e}")
            raise

    def mv(
        self,
        source: PathLike[str] | str,
        dest: PathLike[str] | str
    ):
        source: Path = Path(source)
        dest: Path = Path(dest)
        if not source.exists():
            self._logger.error(f"Directory not found: {source}. Can't move")
            raise FileNotFoundError(f"{source} does not exist")
        try:
            shutil.move(source, dest)
            self._logger.info(f"Moving {source} to {dest}")
        except PermissionError as e:
            self._logger.error("Permission denied")
            raise
    
    def rm(
        self,
        recursive: bool,
        path: PathLike[str] | str
    ) -> None:
        path = Path(path)
        if not path.exists():
            self._logger.error(f"{path} does not exist")
            raise FileNotFoundError("Can't remove file that does not exist")
        if path.absolute() == Path("/") or path.absolute() == Path("..").absolute():
            self._logger.error(f"{path} is either a root or parent directory")
            raise PermissionError("Can't delete root or parent directory")
        if path.is_dir():
            if not recursive:
                self._logger.error(f"Cannot remove {path.name} is a directory")
                raise IsADirectoryError(f"Can't delete {path} -r is required")
            self._logger.info(f"removing {path}")
            shutil.rmtree(path)
        else:
            self._logger.info(f"removing {path}")
            os.remove(path)

    def pack(
        self,
        folder: PathLike[str] | str,
        archive_name: PathLike[str] | str,
        archive_format: Literal[ArchiveFormat.gztar, ArchiveFormat.zipfile]
    ) -> None:
        folder = Path(folder)
        archive_name = Path(archive_name)
        if not folder.exists():
            self._logger.error(f"{folder} does not exist")
            raise FileNotFoundError(f"You entered {folder} an unexisting directory")
        if not folder.is_dir():
            self._logger.error(f"{folder} is not a directory. Archivation unavailable")
            raise NotADirectoryError(f"{folder} is not a directory")
        if archive_name.exists():
            self._logger.error(f"{archive_name.name} already exists")
            raise FileExistsError(f"{archive_name.name} exists. Cant't archive")
        archive_name = Path(os.path.splitext(archive_name)[0])
        self._logger.info("Archiving a directory")
        shutil.make_archive(base_name=archive_name.name, base_dir=str(folder), format=archive_format)
    
    def unpack(
        self,
        archive: PathLike[str] | str,
        dest: PathLike[str] | str,
        archive_format: Literal[ArchiveFormat.gztar, ArchiveFormat.zipfile]
    ) -> None:
        archive = Path(archive)
        dest = Path(dest)
        if not archive.exists():
            self._logger.error("Archive does not exist")
            raise FileNotFoundError(f"{archive} does not exist")
        if not dest.exists():
            self._logger.error("Destination does not exist")
            raise FileNotFoundError(f"{dest} does not exist")
        match archive_format:
            case ArchiveFormat.gztar:
                extension: str = ExtensionName.gztar
            case ArchiveFormat.zipfile:
                extension: str = ExtensionName.zipfile
        if not str(archive).endswith(extension) or not archive.is_file():
            self._logger.error("Invalid format")
            raise WrongFormatError(f"Can't unpack {archive}")
        self._logger.info("Unpacking archive")
        shutil.unpack_archive(archive, dest, archive_format)