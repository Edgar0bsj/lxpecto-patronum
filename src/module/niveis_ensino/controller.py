from pathlib import Path
from src.module.niveis_ensino.dto import NivelDeEnsinoInfos
from src.module.niveis_ensino.tabela.nde_tabela import NivelDeEnsinoTabela
from src.cli.promp.nivel_de_ensino import (
    nivel_de_ensino_menu_prompt,
    file_path_prompt,
)
from src.module.niveis_ensino.service import Service
from src.module.niveis_ensino.err.handle_errs import NivelDeEnsinoError

import pandas as pd
import logging

logger = logging.getLogger(__name__)


class NivelDeEnsinoController:
    def __init__(self):
        self.service = Service()

    def run(self):
        while True:
            choice = nivel_de_ensino_menu_prompt()

            if choice == "Voltar ao Menu Principal" or choice is None:
                break

            match choice:

                case "Visualizar Nivel de Ensino":
                    self._handle_visualizar_nivel_de_ensino()
                    break

                case "Baixar Modelo em Branco (.xlsx)":
                    self._handle_exportar_modelo()
                    input()
                    break

                case "Importar Dados do Excel":
                    self._handle_importe_dados_xlsx()
                    break

                case "Exportar Dados Cadastrados":
                    input("EM DESENVOLVIMENTO")
                    input()

                    break

                case "Excluir Nivel de Ensino":
                    input("EM DESENVOLVIMENTO")
                    input()

                    break

                case _:
                    print("Error")
                    input()
                    break

    # =========================================
    # Utils
    # =========================================
    def get_info(self) -> NivelDeEnsinoInfos:
        infos = self.service.get_info()
        return infos

    # =========================================
    # HANDLES
    # =========================================
    def _handle_visualizar_nivel_de_ensino(self):
        nivel_de_ensino_list = self.service.buscar_todos_nde()
        data = [
            (elem.nome, elem.codigo, elem.tipo_de_nivel)
            for elem in nivel_de_ensino_list
        ]

        table = NivelDeEnsinoTabela()
        table.sett_data(data)
        table.run()

        #
        #
        #
        #
        #

    def _handle_exportar_modelo(self):
        modelo = [
            {
                "name": "",
                "codigo": "",
                "tipo_de_nivel": "",
            }
        ]

        _buffe = pd.DataFrame(modelo)

        _buffe.to_excel("2.niveis_ensino.xlsx", index=False)

        logger.info("Modelo exportado com Sucesso!")

    #
    #
    #
    #
    #
    def _handle_importe_dados_xlsx(self):
        file_path = file_path_prompt()
        file_path = Path(file_path)

        if not file_path.exists():
            raise NivelDeEnsinoError(message="Caminha inválido", obs="Path")

        if file_path.suffix != ".xlsx":
            raise NivelDeEnsinoError(
                message="Tipo de arquivo incompativel", obs=file_path.suffix
            )

        self.service.importar_e_sicronizar_xlsx(file_path=file_path)
        input()
