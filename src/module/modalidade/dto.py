from enum import Enum

from pydantic import BaseModel, field_validator, Field


class TipoModalidade(str, Enum):
    PRESENCIAL = "PRESENCIAL"
    HIBRIDO = "HIBRIDO"
    ENSINO_A_DISTANCIA = "ENSINO_A_DISTANCIA"


class ModalidadeDto(BaseModel):
    id: int | None = None
    nome: str = Field(..., min_length=3, max_length=50)
    codigo: str = Field(..., min_length=3, max_length=50)
    tipo_modalidade: TipoModalidade

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
