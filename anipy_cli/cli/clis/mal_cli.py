from typing import TYPE_CHECKING

from InquirerPy import inquirer

from anipy_cli.cli.clis.base_cli import CliBase
from anipy_cli.cli.menus import MALMenu
from anipy_cli.cli.util import error
from anipy_cli.config import Config
from anipy_cli.error import MyAnimeListError
from anipy_cli.mal import MyAnimeList

if TYPE_CHECKING:
    from anipy_cli.cli.arg_parser import CliArgs


class MalCli(CliBase):
    def __init__(self, options: "CliArgs", rpc_client=None):
        super().__init__(options, rpc_client)
        self.user = ""
        self.password = ""
        self.mal = None

    def print_header(self):
        pass

    def take_input(self):
        config = Config()
        user = config.mal_user
        password = config.mal_password or self.options.mal_password

        if not user:
            self.user = inquirer.text(
                "Your MyAnimeList Username: ",
                validate=lambda x: len(x) > 1,
                invalid_message="You must enter a username!",
                long_instruction="Hint: You can save your username and password in the config!"
            ).execute()

        if not password:
            self.password = inquirer.secret(
                "Your MyAnimeList Password: ",
                transformer=lambda _: "[hidden]",
                validate=lambda x: len(x) > 1,
                invalid_message="You must enter a password!",
                long_instruction="Hint: You can also pass the password via the `--mal-password` option!"
            ).execute()

    def process(self):
        try:
            self.mal = MyAnimeList.from_password_grant(self.user, self.password)
        except MyAnimeListError as e:
            error(f"{str(e)}\nCannot login to MyAnimeList, it is likely your credentials are wrong", fatal=True)

    def show(self):
        pass

    def post(self):
        menu = MALMenu(mal=self.mal, options=self.options, rpc_client=self.rpc_client)

        if self.options.auto_update:
            menu.download(mode="all")
        else:
            menu.run()
