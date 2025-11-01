from enum import Enum

class ArchiveFormat(str, Enum):
    zipfile = ("zip")
    gztar = ("gztar")

class ExtensionName(str, Enum):
    zipfile = (".zip")
    gztar = (".tar.gz")
