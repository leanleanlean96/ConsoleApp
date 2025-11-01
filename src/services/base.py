from abc import ABC, abstractmethod
from os import PathLike
from typing import Literal, Generator, Sequence

from src.enums.file_mode import FileReadMode
from src.enums.archive_format import ArchiveFormat


class OSConsoleServiceBase(ABC):
    @abstractmethod
    def ls(self, path: PathLike[str] | str, all_files: bool, long_form: bool) -> list[str]:
        ...

    @abstractmethod
    def cd(self, path: PathLike[str] | str) -> None:
        ...

    @abstractmethod
    def cp(self, recursive: bool, source: PathLike[str] | str, dest: PathLike[str] | str) -> None:
        ...

    @abstractmethod
    def cat(
        self,
        filename: PathLike[str] | str,
        mode: Literal[FileReadMode.string, FileReadMode.bytes] = FileReadMode.string,
    ) -> str | bytes:
        ...

    @abstractmethod
    def mv(self, source: PathLike[str] | str, dest: PathLike[str] | str) -> None:
        ...

    @abstractmethod
    def rm(self, recursive: bool, path: PathLike[str] | str) -> None:
        ...

    @abstractmethod
    def pack(
        self,
        folder: PathLike[str] | str,
        archive_name: PathLike[str] | str,
        archive_format: Literal[ArchiveFormat.gztar, ArchiveFormat.zipfile]
    ) -> None:
        ...

    @abstractmethod
    def unpack(
        self,
        archive: PathLike[str] | str,
        dest: PathLike[str] | str,
        archive_format: Literal[ArchiveFormat.gztar, ArchiveFormat.zipfile]
    ) -> None:
        ...

    @abstractmethod
    def grep(
        self,
        recursive: bool,
        ignorecase: bool,
        pattern: str,
        files: Sequence[PathLike[str] | str]
    ) -> Generator[str, None, None]:
        ...

    @abstractmethod
    def history(self) -> list[str]:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...

    @abstractmethod
    def undo_mv(self, command: str) -> None:
        ...

    @abstractmethod
    def undo_cp(self, command: str) -> None:
        ...

    @abstractmethod
    def undo_rm(self, command: str) -> None:
        ...
