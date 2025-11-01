import logging
from logging import config
from src.common.config import LOGGING_CONFIG
from src.services.history_service import HistoryService
from src.services.linux_console import LinuxConsoleService

def init_services() -> LinuxConsoleService:
    config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    history = HistoryService()
    console_service = LinuxConsoleService(logger=logger, history_service=history)
    console_service._history.get_history_file()
    return console_service
