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
    tags: str | None = None

    # fk
    aluno_id: str | None

    #
    #
    #
    @field_validator("matricula", mode="before")
    @classmethod
    def normalizar_matricula(cls, value: Any) -> str:
        if not value:
            raise ValueError("O matricula não pode ser vazio.")

        val_str = str(value).strip()

        val_str = re.sub(r"\.0+$", "", val_str)

        return val_str

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
    @field_validator("login", mode="before")
    @classmethod
    def normalizar_login(cls, value: Any) -> str:
        if not value:
            raise ValueError("O login não pode ser vazio.")

        val_str = str(value).strip()

        val_str = re.sub(r"\.0+$", "", val_str)

        return val_str

    #
    #
    #
    @field_validator("senha", mode="before")
    @classmethod
    def normalizar_senha(cls, value: Any) -> str:
        if not value:
            return "Unig@2026"

        val_str = str(value).strip()

        if len(val_str) < 3:
            return "Unig@2026"

        return val_str

    #
    #
    #
    @field_validator("tags", mode="before")
    @classmethod
    def normalizar_tags(cls, value: Any) -> str:
        if not value:
            return ""

        texto_bruto = str(value).strip()
        partes = [item.strip() for item in texto_bruto.split(",") if item.strip()]

        val_str = ", ".join(partes)
        return val_str


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
    tags: str | None = Field(None, description="Filtrar por tags")
