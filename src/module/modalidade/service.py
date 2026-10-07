import pandas as pd
from pydantic import ValidationError
from src.module.modalidade.errs.handle_errs import ModalidadeValidationError

from src.module.modalidade.dto import ModalidadeDto
from src.module.modalidade.repository import Repository
from pandas import DataFrame


class Service:
    def __init__(self):
        self.repo = Repository()

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
