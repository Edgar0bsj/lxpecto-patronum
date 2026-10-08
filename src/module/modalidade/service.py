import pandas as pd
from pydantic import ValidationError
from src.module.modalidade.errs.handle_errs import ModalidadeValidationError

from src.module.modalidade.dto import ModalidadeDto
from src.module.modalidade.repository import Repository
from pandas import DataFrame
from src.module.modalidade.dto import MoldalidadeResponseDto

import logging

logger = logging.getLogger(__name__)


class Service:
    def __init__(self):
        self.repo = Repository()

    #
    #
    #
    #
    #
    #
    #
    def df_to_dto(
        self,
        df: DataFrame,
        colls: dict = {
            "nome": "nome",
            "codigo": "codigo",
            "tipo_de_modalidade": "tipo_de_modalidade",
        },
    ) -> tuple[list[ModalidadeDto], list]:

        box: list[ModalidadeDto] = []
        box_erros: list[ValidationError] = []
        for _, v in df.iterrows():
            try:
                box.append(
                    ModalidadeDto(
                        nome=v[colls["nome"]],
                        codigo=v[colls["codigo"]],
                        tipo_modalidade=v[colls["tipo_de_modalidade"]],
                    )
                )
            except ValidationError as err:
                box_erros.append(err)

        codigos = set()
        codigos_duplicado = set()
        for e in box:
            if e.codigo in codigos:
                codigos_duplicado.add(e.codigo)
            else:
                codigos.add(e.codigo)

        if len(codigos_duplicado) > 0:
            raise ModalidadeValidationError(
                message="Código duplicado", field=codigos_duplicado
            )

        return (box, box_erros)

    #
    #
    #
    #
    #
    #
    #
    def import_all_sicronize(self, mod_dtos: list[ModalidadeDto]) -> tuple[int, int]:
        exist = []
        not_exist = []

        for mod in mod_dtos:
            result = self.repo.find_by_cod(mod.codigo)

            if result:
                exist.append(result)
                continue

            not_exist.append(mod)

        for item in not_exist:
            self.repo.save(item)

        for updat in exist:
            self.repo.edit(updat)

        return (len(not_exist), len(exist))

    def find_last_update(self):
        result = self.repo.find_by_last_update()

        return result

    #
    #
    #
    #
    #
    #
    #
    def export_modelo(self):
        tamplete_mod = [
            {
                "nome": "",
                "codigo": "",
                "tipo_de_modalidade": "",
            }
        ]

        df = pd.DataFrame(tamplete_mod)

        df.to_excel("1.modalidades.xlsx", index=False)
        return

    #
    #
    #
    #
    #
    #
    #
    def pegar_todas_modalidades(
        self, to_dict=False
    ) -> list[dict] | list[MoldalidadeResponseDto]:
        result = self.repo.find_all()
        if not to_dict:
            result = [
                MoldalidadeResponseDto(
                    nome=e.nome, codigo=e.codigo, tipo_modalidade=e.tipo_modalidade
                )
                for e in result
            ]
        else:
            result = [
                {
                    "nome": e.nome,
                    "codigo": e.codigo,
                    "tipo_modalidade": e.tipo_modalidade,
                }
                for e in result
            ]

        return result

    #
    #
    #
    #
    #
    #
    #
    def excluir_modalidade(self, cod: str) -> bool:
        mod = self.repo.find_by_cod(cod)

        if not mod:
            logger.error(f"Modalidade com o Código {cod} não encontrado!")
            return False

        self.repo.delete(mod.id)
        logger.info(f"Modalidade:{mod.nome} Deletado com Sucesso! ")
        return True
