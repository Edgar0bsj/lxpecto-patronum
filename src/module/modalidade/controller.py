from pathlib import Path

from src.cli.promp.modalidade import file_path_prompt
from src.cli.promp.modalidade import modalidade_menu_prompt
from src.module.modalidade.service import Service
import pandas as pd


class ModalidadeController:
    def __init__(self):
        self.service = Service()

    def run(self):
        while True:
            choice = modalidade_menu_prompt()

            if choice == "Voltar" or choice is None:
                break

            match choice:

                case "Importar via Excel":
                    print("EM DESENVOLVIMENTO")
                    input()
                    self._handle_import_mod_excel()

                    break

                case "Deletar via Excel":
                    print("EM DESENVOLVIMENTO")
                    input()

                    break

                case "Exportar em Excel":
                    print("EM DESENVOLVIMENTO")
                    input()

                    break

                case _:
                    print("Error")
                    input()
                    break

    # =========================================
    # Utils
    # =========================================
    def get_info(self):
        last_update = self.service.find_last_update()

        if not last_update:
            return {"date": "-", "time": "-"}

        return {"date": str(last_update.date()), "time": str(last_update.time())}

    # =========================================
    # HANDLES
    # =========================================
    def _handle_import_mod_excel(self):
        file_path = file_path_prompt()
        file_path = Path(file_path)

        if not file_path.exists():
            print("Error: path invalido !")
            input()
            return

        if file_path.suffix != ".xlsx":
            print("Error: O arquivo não é xlsx")
            input()
            return

        df = pd.read_excel(file_path)

        list_mod_dto, box_errs = self.service.df_to_dto(df)

        if len(box_errs) > 0:
            for erro in box_errs:
                print("================================================")
                print("--  ERROR  --")
                print("================================================")
                print("LINHA->", erro["linha"])
                print("MENSAGEM->", erro["msg"])
            input()
            return

        created_cont, updated_cont = self.service.import_all_sicronize(list_mod_dto)

        print("Novo", created_cont)
        print("Atualizado", updated_cont)
        input()
