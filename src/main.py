from src.config.logging import setup_logging

from pathlib import Path
import sys

from rich import print
from rich.panel import Panel

from src.module.parametros.controller import ParametroController
from src.module.modalidade.controller import ModalidadeController
from src.cli.promp.parametro import main_menu_prompt
from src.module.util.clear_terminal import clear_terminal

setup_logging()


def main():
    clear_terminal()
    file_path = Path("Planilha_Mestre.xlsx")

    parametroController = ParametroController()
    modalidadeController = ModalidadeController()

    while True:
        paramInfo = parametroController.get_info()
        modInfo = modalidadeController.get_info()
        info = (
            f"[bold white]Nome da Unidade:[/bold white] [bold green]{paramInfo['nome']}[/bold green]\n"
            f"[bold white]Sigla da Unidade:[/bold white] [bold green]{paramInfo['sigla']}[/bold green]\n"
            f"[bold white]GPA:[/bold white]              [bold green]{paramInfo['gpa']}[/bold green]\n"
            f"[bold white]NPJ:[/bold white]              [bold green]{paramInfo['npj']}[/bold green]\n\n"
            f"[bold cyan]--- ULTIMA IMPORTAÇÕES ---[/bold cyan]\n"
            f"[bold white]Modalidade:[/bold white]       [bold green]{modInfo["last_update"]}[/bold green]\n"
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

            case "Modalidade":
                modalidadeController.run()

            case _:
                print("Error")
                return "_"

        clear_terminal()


if "__main__" == __name__:
    main()
