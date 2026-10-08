from pathlib import Path

from src.module.niveis_ensino.repository import Repository
from src.module.niveis_ensino.dto import NivelDeEnsinoDto, NivelDeEnsinoInfos
from src.module.niveis_ensino.domain import NivelDeEnsino
from src.module.niveis_ensino.err.handle_errs import NivelDeEnsinoError

import pandas as pd

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
    #
    #
    def criar_nivel_de_ensino(
        self, nome: str, codigo: str, tipo_de_nivel: str
    ) -> NivelDeEnsinoDto:
        ndeDto = NivelDeEnsinoDto(nome=nome, codigo=codigo, tipo_de_nivel=tipo_de_nivel)

        self.repo.save(ndeDto=ndeDto)

        return ndeDto

    #
    #
    #
    #
    #
    #
    #
    #
    #
    def editar_nivel_de_ensino(
        self, id: int, nome: str, codigo: str, tipo_de_nivel: str
    ) -> NivelDeEnsinoDto:
        ndeDto = NivelDeEnsinoDto(
            id=id, nome=nome, codigo=codigo, tipo_de_nivel=tipo_de_nivel
        )
        self.repo.edit(ndeDto=ndeDto)

        return ndeDto

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def buscar_todos_nde(self) -> list[NivelDeEnsinoDto]:
        todos_nde: list[NivelDeEnsino] = self.repo.find_all()

        if len(todos_nde) == 0:
            return []

        response = [
            NivelDeEnsinoDto(
                id=e.id, nome=e.nome, codigo=e.codigo, tipo_de_nivel=e.tipo_de_nivel
            )
            for e in todos_nde
        ]

        return response

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def buscar_por_id(self, id: int) -> NivelDeEnsinoDto:
        result = self.repo.find_by_id(id)

        if not result:
            return None

        return NivelDeEnsinoDto(
            id=result.id,
            nome=result.nome,
            codigo=result.codigo,
            tipo_de_nivel=result.tipo_nivel,
        )

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def buscar_por_codigo(self, codigo: str):

        result = self.repo.find_by_cod(codigo)

        if not result:
            return None

        return NivelDeEnsinoDto(
            id=result.id,
            nome=result.nome,
            codigo=result.codigo,
            tipo_de_nivel=result.tipo_nivel,
        )

    #
    #
    #
    #
    #
    #
    #
    #
    #
    def deletar_nde(self, id: int) -> bool:
        return self.repo.delete(id)

    #
    #
    #
    #
    #
    #
    #
    #
    #
    def get_info(self) -> NivelDeEnsinoInfos:
        all_entity = self.repo.find_all()
        last_update = self.repo.find_by_last_update()

        if last_update:
            last_update = str(last_update.date())
        else:
            last_update = "-"

        qtd_registro = len(all_entity)
        res = NivelDeEnsinoInfos(qtd_registro=qtd_registro, ultimo_registro=last_update)
        return res

    #
    #
    #
    #
    #
    #
    #
    #
    #
    def importar_e_sicronizar_xlsx(
        self,
        file_path: Path,
        *,
        col_name="name",
        col_cod="codigo",
        col_tipo_de_nivel="tipo_de_nivel",
    ):
        list_nde = pd.read_excel(file_path).to_dict("records")

        box_ndeDtos: list[NivelDeEnsinoDto] = []
        for row in list_nde:
            nome = str(row[col_name])
            codigo = str(row[col_cod])
            tipo_de_nivel = str(row[col_tipo_de_nivel])

            ndeDto = NivelDeEnsinoDto(
                nome=nome, codigo=codigo, tipo_de_nivel=tipo_de_nivel
            )

            box_ndeDtos.append(ndeDto)

        # ---

        temp_codigo = set()
        codigo_duplicados = set()

        for ndeDto in box_ndeDtos:

            if ndeDto.codigo in temp_codigo:
                codigo_duplicados.add(ndeDto)
                continue

            temp_codigo.add(ndeDto.codigo)

        if len(codigo_duplicados) != 0:
            raise NivelDeEnsinoError(message="Codigo Duplicado", obs=codigo_duplicados)

        # ---

        _buffer_registro_salvar = []
        _buffer_registro_atualizar = []

        for elem in box_ndeDtos:
            isExist = self.repo.find_by_cod(elem.codigo)

            if isExist:
                elem.id = isExist.id
                _buffer_registro_atualizar.append(elem)
                continue

            _buffer_registro_salvar.append(elem)

        # ---

        [self.repo.save(item) for item in _buffer_registro_salvar]
        [self.repo.edit(item) for item in _buffer_registro_atualizar]

        logger.info(f"Nivel de Ensino | {len(box_ndeDtos)} total de registros")
        logger.info(f"Nivel de Ensino | {len(_buffer_registro_salvar)} foram inseridos")
        logger.info(
            f"Nivel de Ensino | {len(_buffer_registro_atualizar)} foram atualizados"
        )
