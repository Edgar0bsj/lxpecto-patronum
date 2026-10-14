import re
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_validator


class AlunoRequest(BaseModel):
    nome: Annotated[str, Field(min_length=3, max_length=150)]
    cpf: Annotated[str, Field(min_length=11, max_length=11)]
    login: Annotated[str, Field(min_length=3, max_length=100)]
    senha: Annotated[str, Field(min_length=3, max_length=100)]

    #
    #
    #
    #
    @field_validator("nome", mode="before")
    @classmethod
    def normalizar_nome(cls, value: Any) -> str:

        if value is None:
            raise ValueError("Não deve ser Nulo")

        val_str = str(value).strip().lower()

        return val_str

    #
    #
    #
    #
    #
    #
    @field_validator("cpf", mode="before")
    @classmethod
    def normalizar_cpf(cls, value: Any) -> str:
        if value is None:
            raise ValueError("O cpf não pode ser vazio.")

        val_str = str(value).strip()

        # Remove casas decimais no final (ex: .0 ou .00 comuns vindas do Excel/Pandas)
        val_str = re.sub(r"\.0+$", "", val_str)

        # Remove tudo o que não for dígito (pontos, traços, letras, etc.)
        cpf_limpo = re.sub(r"\D", "", val_str)

        cpf_limpo = cpf_limpo.zfill(11)

        if len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos.")

        return cpf_limpo

    #
    #
    #
    #
    @field_validator("login", mode="before")
    @classmethod
    def normalizar_login(cls, value: Any) -> str:
        if value is None:
            raise ValueError("O login não pode ser vazio.")

        val_str = str(value).strip().lower()
        val_str = re.sub(r"\.0+$", "", val_str)

        return val_str

    #
    #
    #
    #
    #
    @field_validator("senha", mode="before")
    @classmethod
    def normalizar_senha(cls, value: Any) -> str:
        if value is None:
            return "Unig@2026"

        val_str = str(value).strip()

        return val_str


#
#
#
#
#
#
#
class AlunoFiltro(BaseModel):
    nome: str | None = Field(None, description="Filtrar por parte do nome")
    codigo_externo: str | None = Field(
        None, description="Filtrar por parte do codigo externo"
    )

    cpf: str | None = Field(None, description="Filtrar por parte do cpf")
    login: str | None = Field(None, description="Filtrar por parte do login")
