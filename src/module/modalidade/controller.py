from pathlib import Path

from src.cli.promp.modalidade import file_path_prompt
from src.cli.promp.modalidade import modalidade_menu_prompt
from src.module.modalidade.service import Service
import pandas as pd

from src.module.modalidade.decorator.handle_exceptions import handle_exceptions
from src.module.modalidade.errs.handle_errs import ModalidadeValidationError


import logging

logger = logging.getLogger(__name__)


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
    @handle_exceptions
    def _handle_import_mod_excel(self):
        file_path = file_path_prompt()
        file_path = Path(file_path)

        if not file_path.exists():
            raise ModalidadeValidationError(message="Caminha inválido", field="Path")

        if file_path.suffix != ".xlsx":
            raise ModalidadeValidationError(
                message="Tipo de arquivo incompativel", field=file_path.suffix
            )

        df = pd.read_excel(file_path)

        list_mod_dto, box_errs = self.service.df_to_dto(df)

        if len(box_errs) > 0:
            raise ModalidadeValidationError(
                message="Error de validação", field=box_errs
            )

        created_cont, updated_cont = self.service.import_all_sicronize(list_mod_dto)

        logger.info(f"Modalidade Novas: {created_cont}")
        logger.info(f"Modalidade Atualizadas: {updated_cont}")

        input()
