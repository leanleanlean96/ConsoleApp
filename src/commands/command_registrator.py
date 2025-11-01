from typer_shell import make_typer_shell # type: ignore

from src.commands.ls import register_ls
from src.commands.cd import register_cd
from src.commands.cat import register_cat
from src.commands.cp import register_cp
from src.commands.mv import register_mv
from src.commands.rm import register_rm
from src.commands.tar import register_tar
from src.commands.zip import register_zip
from src.commands.grep import register_grep
from src.commands.history import register_history

def create_app():
    app = make_typer_shell(prompt="$~ ")

    # Register all commands
    app = register_ls(app)
    app = register_cd(app)
    app = register_cat(app)
    app = register_cp(app)
    app = register_mv(app)
    app = register_rm(app)
    app = register_tar(app)
    app = register_zip(app)
    app = register_grep(app)
    app = register_history(app)

    return app
