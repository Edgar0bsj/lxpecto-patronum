from pathlib import Path
import sys

from rich import print
from rich.panel import Panel

from src.module.parametros.controller import ParametroController
from src.cli.prompts import *
from src.module.util.clear_terminal import clear_terminal


def main():
    file_path = Path("Planilha_Mestre.xlsx")

    parametroController = ParametroController()

    while True:
        paramInfo = parametroController.get_param()
        info = (
            f"[bold white]Nome da Unidade:[/bold white] {paramInfo['nome']}\n"
            f"[bold white]Sigla da Unidade:[/bold white] {paramInfo['sigla']}\n"
            f"[bold white]GPA:[/bold white]              {paramInfo['gpa']}\n"
            f"[bold white]NPJ:[/bold white]              {paramInfo['npj']}"
        )
        print(
            Panel(info, title="[bold cyan]LXPectro Patronum[/bold cyan]", expand=False)
        )

        choice = main_menu_prompt()

        if choice is None or choice == "Sair":
            print("\nSaindo da aplicação...")
            sys.exit(0)

        match choice:

            case "Parametros":
                parametroController.run()

            case _:
                print("Error")
                return "_"

        clear_terminal()


if "__main__" == __name__:
    main()
