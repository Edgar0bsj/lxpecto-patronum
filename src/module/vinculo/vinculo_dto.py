import re

from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Any

from enum import Enum


class ModalidadeType(str, Enum):
    EAD = "ead"
    PRESENCIAL = "presencial"
    SEMI_PRESENCIAL = "semi_presencial"


class PoloType(str, Enum):
    UNIG = "unig"
    UNIG_HIBRIDO = "unig_hibrido"
    ITAPERUNA = "itaperuna"
    UNIABEL = "uniabel"
    LIFE_UNIC = "life_unic"


class VinculoDto(BaseModel):
    matricula: Annotated[str, Field(min_length=3, max_length=100)]
    modalidade: ModalidadeType
    polo: PoloType
    email: Annotated[str, Field(min_length=3, max_length=100)]
    status: bool = True

    aluno_id: str

    #
    #
    #
    #
    #
    #
    #
    @field_validator("matricula", mode="before")
    @classmethod
    def normalizar_matricula(cls, value: Any) -> str:
        if value is None:
            raise ValueError("O matricula não pode ser vazio.")

        val_str = str(value).strip().lower()
        val_str = re.sub(r"\.0+$", "", val_str)

        return val_str

    #
    #
    #
    #
    #
    @field_validator("email", mode="before")
    @classmethod
    def normalizar_email(cls, value: Any) -> str:
        if not value:
            raise ValueError("O e-mail não pode ser vazio.")

        val_str = str(value).strip()

        email_limpo = val_str.lower()

        regex_email = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"

        if not re.match(regex_email, email_limpo):
            raise ValueError("O e-mail informado possui um formato inválido.")

        return email_limpo


#
#
#
#
#
class VinculoFiltro(BaseModel):
    matricula: str | None = Field(None, description="Filtrar por parte do matricula")
    modalidade: ModalidadeType | None = Field(
        None, description="Filtrar por parte do matricula"
    )
    polo: PoloType | None = Field(None, description="Filtrar por parte do matricula")
    email: str | None = Field(None, description="Filtrar por parte do email")
    status: bool | None = Field(None, description="Filtrar por status")
