from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, field_validator, Field


class TipoNivel(str, Enum):
    GRADUACAO = "GRADUACAO"
    POS_GRADUACAO = "POS_GRADUACAO"
    ENSINO_MEDIO = "ENSINO_MEDIO"
    CURSO_DE_EXTERNSAO = "CURSO_DE_EXTERNSAO"


class NivelDeEnsinoDto(BaseModel):
    id: int | None = None
    nome: str = Field(..., min_length=3, max_length=50)
    codigo: str = Field(..., min_length=3, max_length=50)
    tipo_de_nivel: TipoNivel

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


@dataclass
class NivelDeEnsinoInfos:
    qtd_registro: int
    ultimo_registro: str
