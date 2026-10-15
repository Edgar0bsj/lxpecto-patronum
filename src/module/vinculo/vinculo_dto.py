import re

from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Any


class VinculoDto(BaseModel):
    matricula: Annotated[str, Field(min_length=3, max_length=100)]
    email: Annotated[str, Field(min_length=3, max_length=100)]
    status: bool
    login: Annotated[str, Field(min_length=3, max_length=100)]
    senha: Annotated[str, Field(min_length=3, max_length=100)]
    is_primary: bool = True

    # fk
    aluno_id: Annotated[str, Field(min_length=3, max_length=100)]

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
class VinculoFiltro(BaseModel):
    matricula: str | None = Field(None, description="Filtrar por parte do matricula")
    email: str | None = Field(None, description="Filtrar por parte do email")
    status: bool | None = Field(None, description="Filtrar por status")
    login: str | None = Field(None, description="Filtrar por parte do login")
    is_primary: bool | None = Field(None, description="Filtrar por is_primary")
    aluno_id: str | None = Field(None, description="Filtrar por aluno_id")
