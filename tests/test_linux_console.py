import os
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.enums.file_mode import FileReadMode
from src.enums.archive_format import ArchiveFormat
from src.services.linux_console import LinuxConsoleService


class TestLinuxConsoleService:

    def test_cd_valid(self, service: LinuxConsoleService, fs: FakeFilesystem):
        service.cd("/home/user/EvilArthas")
        service._logger.info.assert_called_with("Changing directory to /home/user/EvilArthas")

    def test_cd_not_existing_dir(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            service.cd("/BOJlWE6CTBO")
        service._logger.error.assert_called_with("Folder not found: /BOJlWE6CTBO")

    def test_cd_to_file(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/home/user/Niceych.txt")
        with pytest.raises(NotADirectoryError):
            service.cd("/home/user/Niceych.txt")
        service._logger.error.assert_called_with("You entered /home/user/Niceych.txt is not a directory")

    def test_ls_default(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/EvilArthas")
        fs.create_file("/EvilArthas/file1.txt")
        fs.create_file("/EvilArthas/file2.txt")

        result = service.ls("/EvilArthas", all_files=False, long_form=False)

        assert len(result) == 2
        assert "file1.txt\n" in result
        assert "file2.txt\n" in result

    def test_ls_not_all_not_long(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/test")
        fs.create_file("/test/.invisible")
        fs.create_file("/test/visible.txt")

        result = service.ls("/test", all_files=False, long_form=False)

        assert len(result) == 1
        assert "visible.txt\n" in result
        assert ".invisible\n" not in result

    def test_ls_show_all(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/test")
        fs.create_file("/test/.shadow_blade")
        fs.create_file("/test/visible.txt")

        result = service.ls("/test", all_files=True, long_form=False)

        assert len(result) == 2
        assert ".shadow_blade\n" in result

    def test_ls_directory_not_found(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            service.ls("/BOJlWE6CTBO", all_files=False, long_form=False)
        service._logger.error.assert_called_with("Folder not found: /BOJlWE6CTBO")

    def test_ls_path_is_file(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/Hailrake.txt")
        with pytest.raises(NotADirectoryError):
            service.ls("/Hailrake.txt", all_files=False, long_form=False)
        service._logger.error.assert_called_with("You entered /Hailrake.txt is not a directory")

    def test_cp_file_success(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/source.txt", contents="file content")
        service.cp(False, "/source.txt", "/dest.txt")
        assert os.path.exists("/dest.txt")
        with open("/dest.txt", 'r') as f:
            assert f.read() == "file content"

    def test_cp_directory_recursive(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/source")
        fs.create_file("/source/file1.txt")
        service.cp(True, "/source", "/backup")
        assert os.path.exists("/backup/file1.txt")

    def test_cp_directory_recursive_false(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/source")
        with pytest.raises(IsADirectoryError):
            service.cp(False, "/source", "/backup")
        service._logger.error.assert_called_with("Can't copy dir with recursive=False")

    def test_cp_source_not_found(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            service.cp(False, "/BOJlWE6CTBO", "/dest")
        service._logger.error.assert_called_with("Folder not found")

    def test_rm_file_success(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/Hailrake.txt")
        service.rm(False, "/Hailrake.txt")
        assert not os.path.exists("/Hailrake.txt")

    def test_rm_directory_recursive(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/Arthas")
        fs.create_file("/Arthas/file.txt")
        service.rm(True, "/Arthas")
        assert not os.path.exists("/Arthas")

    def test_rm_directory_withot_recursive(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/dir")
        with pytest.raises(IsADirectoryError):
            service.rm(False, "/dir")
        service._logger.error.assert_called_with("Cannot remove a directory with recursive=false")

    def test_rm_nonexistent_path(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            service.rm(False, "/BOJlWE6CTBO")
        service._logger.error.assert_called_with("Path does not exist")

    # MV Command Tests
    def test_mv_file_success(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/old.txt", contents="content")
        service.mv("/old.txt", "/new.txt")
        assert not os.path.exists("/old.txt")
        assert os.path.exists("/new.txt")
        with open("/new.txt", 'r') as f:
            assert f.read() == "content"

    def test_mv_source_not_found(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            service.mv("/BOJlWE6CTBO", "/new")
        service._logger.error.assert_called_with("Directory not found Can't move")

    def test_cat_file_text_mode(self, service: LinuxConsoleService, fs: FakeFilesystem):
        content = "hi hi hih hi"
        fs.create_file("/test.txt", contents=content)
        result = service.cat("/test.txt", FileReadMode.string)
        assert result == content

    def test_cat_file_bytes_mode(self, service: LinuxConsoleService, fs: FakeFilesystem):
        content = b"Binary content"
        fs.create_file("/test.bin", contents=content)
        result = service.cat("/test.bin", FileReadMode.bytes)
        assert result == content

    def test_cat_not_existing_file(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            service.cat("/nonexistent.txt", FileReadMode.string)
        service._logger.error.assert_called_with("File not found: /nonexistent.txt")

    def test_cat_directory_error(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/testdir")
        with pytest.raises(IsADirectoryError):
            service.cat("/testdir", FileReadMode.string)
        service._logger.error.assert_called_with("Entered filename is not a file")

    def test_grep_file_valid(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/test.txt", contents="Privet\nPoka\nAAAAAAAA")
        results = list(service.grep(False, False, "Poka", ["/test.txt"]))
        assert len(results) == 1
        assert "pattern" in results[0]

    def test_grep_file_pattern_not_found(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/test.txt", contents="jhaslhfAJSHFklj\noffsadoak")
        results = list(service.grep(False, False, "pattern", ["/test.txt"]))
        assert len(results) == 0

    def test_grep_recursive_directory(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/dir")
        fs.create_file("/dir/file1.txt", contents="asdasd")
        fs.create_file("/dir/file2.txt", contents="oaoaoaoao")
        results = list(service.grep(True, False, "asdasd", ["/dir"]))
        assert len(results) == 1

    def test_grep_ignore_case(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/test.txt", contents="AAAAA")
        results = list(service.grep(False, True, "aaa", ["/test.txt"]))
        assert len(results) == 1

    def test_grep_file_not_found(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            list(service.grep(False, False, "pattern", ["/net.txt"]))

    def test_grep_directory_without_recursive_raises_error(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/dir")
        with pytest.raises(IsADirectoryError):
            list(service.grep(False, False, "pattern", ["/dir"]))
        service._logger.error.assert_called_with("-r unspecified and file is a directory")

    def test_pack_directory_success(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/data")
        fs.create_file("/data/file1.txt", contents="test")
        service.pack("/data", "/archive.zip", ArchiveFormat.zipfile)
        service._logger.info.assert_called_with("Archiving a directory")

    def test_pack_nonexistent_directory(self, service: LinuxConsoleService, fs: FakeFilesystem):
        with pytest.raises(FileNotFoundError):
            service.pack("/doesnotexist", "/archive.zip", ArchiveFormat.zipfile)
        service._logger.error.assert_called_with("folder does not exist")

    def test_pack_file(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/file.txt")
        with pytest.raises(NotADirectoryError):
            service.pack("/file.txt", "/archive.zip", ArchiveFormat.zipfile)
        service._logger.error.assert_called_with("folder is not a directory. Archivation unavailable")

    def test_unpack_archive_invalid_format(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/archive.zip")
        fs.create_dir("/extract")
        with pytest.raises(Exception):
            service.unpack("/archive.zip", "/extract", ArchiveFormat.zipfile)

    def test_unpack_archive_not_found(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_dir("/extract")
        with pytest.raises(FileNotFoundError):
            service.unpack("/nonexistent.zip", "/extract", ArchiveFormat.zipfile)
        service._logger.error.assert_called_with("Archive does not exist")

    def test_unpack_destination_not_found(self, service: LinuxConsoleService, fs: FakeFilesystem):
        fs.create_file("/archive.zip")
        with pytest.raises(FileNotFoundError):
            service.unpack("/archive.zip", "/nonexistent", ArchiveFormat.zipfile)
        service._logger.error.assert_called_with("Destination does not exist")

    def test_history_success(self, service: LinuxConsoleService, fs: FakeFilesystem):
        service._history.get_history.return_value = [
            (1, "ls /home"),
            (2, "cd /tmp")
        ]
        result = service.history()
        assert len(result) == 2
        assert "1: ls /home" in result[0]
        service._logger.info.assert_called_with("Listing history...")
