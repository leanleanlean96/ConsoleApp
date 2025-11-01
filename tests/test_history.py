from src.services.history_service import HistoryService


class TestHistoryService:

    def test_get_history_with_commands(self, fs):
        history_content = "ls -la /burger\ncd /EvilArthas\ncat ai_avenger\n"
        fs.create_file("src/.history", contents=history_content)
        service = HistoryService()

        result = service.get_history()

        expected = [
            (1, "ls -la /burger"),
            (2, "cd /EvilArthas"),
            (3, "cat ai_avenger")
        ]
        assert result == expected

    def test_append_command_to_hist(self, fs):
        fs.create_file("src/.history", contents="ls\n")
        service = HistoryService()

        service.append_command_to_history("tar DiscreteMath DoNotTouch.tar.gz")

        with open(service.history_file, 'r') as f:
            content = f.read()
        assert content == "ls\ntar DiscreteMath DoNotTouch.tar.gz\n"


    def test_append_and_get_hist(self, fs):
        service = HistoryService()
        fs.create_file("src/.history")
        commands = ["ls", "cd /home", "ls -la /", "cat file.txt"]
        for cmd in commands:
            service.append_command_to_history(cmd)

        history = service.get_history()
        assert len(history) == 4
