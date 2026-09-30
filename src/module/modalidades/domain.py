from pathlib import Path

from pydantic import BaseModel, field_validator
from enum import Enum
import pandas as pd


class TipoModalidade(str, Enum):
    PRESENCIAL = "PRESENCIAL"
    HIBRIDO = "HIBRIDO"
    ENSINO_DISTANCIA = "ENSINO_DISTANCIA"


class Modalidades(BaseModel):
    nome: str
    codigo: str
    tipo_modalidade: TipoModalidade

    # =========================================
    # CREATER
    # =========================================
    @classmethod
    def read_excel(
        cls,
        file_path: Path,
        aba="1.1 Modalidades",
        colls={
            "nome": "Nome *",
            "codigo": "Código *",
            "tipo_modalidade": "Tipo de Modalidade *",
        },
    ) -> list["Modalidades"]:
        df = pd.read_excel(file_path, sheet_name=aba)

        box = []
        for _, v in df.iterrows():
            entity = cls(
                nome=v[colls["nome"]],
                codigo=v[colls["codigo"]],
                tipo_modalidade=v[colls["tipo_modalidade"]],
            )
            box.append(entity)

        return box

    # =========================================
    # TO MANAGER
    # =========================================
    def to_manager(self) -> dict:

        type_modality = None

        if self.tipo_modalidade is TipoModalidade.ENSINO_DISTANCIA:
            type_modality = "distance_learning"

        if self.tipo_modalidade is TipoModalidade.HIBRIDO:
            type_modality = "blended_learning "

        if self.tipo_modalidade is TipoModalidade.PRESENCIAL:
            type_modality = "face_to_face"

        return {
            "name": self.nome,
            "externalId": self.codigo,
            "teachingModalityTypeId": type_modality,
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
