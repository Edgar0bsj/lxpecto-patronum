from pathlib import Path

from pydantic import BaseModel, field_validator
from enum import Enum
import pandas as pd


class TipoNivel(str, Enum):
    GRADUACAO = "GRADUACAO"
    POS_GRADUACAO = "POS_GRADUACAO"
    ENSINO_MEDIO = "ENSINO_MEDIO"
    CURSO_DE_EXTERNSAO = "CURSO_DE_EXTERNSAO"


class NivelEnsino(BaseModel):
    nome: str
    codigo: str
    tipo_nivel: TipoNivel

    # =========================================
    # CREATER
    # =========================================
    @classmethod
    def read_excel(
        cls,
        file_path: Path,
        aba="1.2 Niveis Ensino",
        colls={
            "nome": "Nome *",
            "codigo": "Código *",
            "tipo_nivel": "Tipo de Nível *",
        },
    ) -> list["NivelEnsino"]:
        df = pd.read_excel(file_path, sheet_name=aba)

        box = []
        for _, v in df.iterrows():
            entity = cls(
                nome=v[colls["nome"]],
                codigo=v[colls["codigo"]],
                tipo_nivel=v[colls["tipo_nivel"]],
            )
            box.append(entity)

        return box

    # =========================================
    # TO MANAGER
    # =========================================
    def to_manager(self) -> dict:

        type_nivel = None

        if self.tipo_nivel is TipoNivel.GRADUACAO:
            type_nivel = "graduate"

        if self.tipo_nivel is TipoNivel.POS_GRADUACAO:
            type_nivel = "blended_learning "

        if self.tipo_nivel is TipoNivel.ENSINO_MEDIO:
            type_nivel = "high_school"

        if self.tipo_nivel is TipoNivel.CURSO_DE_EXTERNSAO:
            type_nivel = "extension_course"

        return {
            "name": self.nome,
            "externalId": self.codigo,
            "educationLevelTypeId": type_nivel,
        }

    # =========================================
    # VALIDATORS
    # =========================================
    @field_validator("nome")
    @classmethod
    def normalizar_nome(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("codigo")
    @classmethod
    def normalizar_codigo(cls, value: str) -> str:
        return value.strip().lower()
