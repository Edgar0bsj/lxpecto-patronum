import logging
from pathlib import Path

from datetime import datetime
from src.cli.promp.modalidade import file_path_prompt
from src.cli.promp.modalidade import modalidade_menu_prompt
from src.module.modalidade.service import Service
import pandas as pd

from src.module.modalidade.decorator.handle_exceptions import handle_exceptions
from src.module.modalidade.errs.handle_errs import ModalidadeValidationError

logger = logging.getLogger(__name__)


class ModalidadeController:
    def __init__(self):
        self.service = Service()

    def run(self):
        while True:
            choice = modalidade_menu_prompt()

            if choice == "Voltar ao Menu Principal" or choice is None:
                break

            match choice:

                case "Baixar Modelo em Branco (.xlsx)":
                    self._handle_exportar_modelo()
                    input()
                    break

                case "Importar Dados do Excel":
                    self._handle_import_mod_excel()
                    break

                case "Exportar Dados Cadastrados":
                    # -----------------------------------------
                    # EM DESENVOLVIMENTO
                    # -----------------------------------------
                    self._handle_exportar_all_data()
                    input()

                    break

                case "Excluir Dados via Excel":
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
            return {"last_update": "-"}

        return {"last_update": str(last_update.date())}

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

        print(f"Modalidade Novas: {created_cont}")
        print(f"Modalidade Atualizadas: {updated_cont}")

        input()

    #
    #
    #
    #
    #
    #
    @handle_exceptions
    def _handle_exportar_modelo(self):
        self.service.export_modelo()
        logger.info("Modelo feito com Sucesso!")

    #
    #
    #
    #
    #
    #
    @handle_exceptions
    def _handle_exportar_all_data(self):
        all_modalidades = self.service.pegar_todas_modalidades(to_dict=True)

        df = pd.DataFrame(all_modalidades)

        arquivo_name = f"1.modalidades_{datetime.now():%Y-%m-%d}.xlsx"

        df.to_excel(arquivo_name, index=False)

        logger.info("Planilha de Todas as Modalidades exportada com Sucesso!")
        logger.info(f"Quantidade de registros exportados {len(all_modalidades)}")
