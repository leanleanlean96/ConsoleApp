import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_logger():
    return Mock()

@pytest.fixture
def mock_history_service():
    mock_history = Mock()
    mock_history.get_history.return_value = []
    return mock_history

@pytest.fixture
def service(mock_logger, mock_history_service):
    from src.services.linux_console import LinuxConsoleService
    return LinuxConsoleService(mock_logger, mock_history_service)

@pytest.fixture
def fs(fs):
    fs.create_dir("/home/user")
    fs.create_dir("/home/user/DiscreteMath")
    fs.create_dir("/home/user/EvilArthas")
    return fs
