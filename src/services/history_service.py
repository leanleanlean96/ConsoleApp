from pathlib import Path

class HistoryService:
    def __init__(
        self,
        history_file: Path = Path("src/.history")
        ):
        self.history_file = history_file

    def get_history_file(self) -> None:
        try:
            if not self.history_file.exists():
                self.history_file.touch()
        except Exception:
            raise FileNotFoundError("Could not create history file")

    def get_history(
        self
    ) -> list[tuple[int, str]]:
        try:
            if self.history_file.exists():
                history: list[tuple[int, str]] = [(line, command) for line, command in enumerate(self.history_file.read_text(encoding="utf-8").splitlines(), 1)]
                return history
            return []
        except Exception:
            raise FileNotFoundError("Could not load history")

    def append_command_to_history(
            self,
            cmd: str
    ):
        try:
            if self.history_file.exists():
                with self.history_file.open("a", encoding="utf-8") as h:
                    h.write(cmd + "\n")
        except Exception:
            raise FileNotFoundError("Could not append command to history")
