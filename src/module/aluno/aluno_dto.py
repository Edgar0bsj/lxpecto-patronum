import re
from dataclasses import asdict, dataclass
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_validator

NomeType = Annotated[str, Field(min_length=3, max_length=150)]
CpfType = Annotated[str, Field(min_length=11, max_length=11)]


# ===================================================
# AlunoCreate
# ===================================================
class AlunoCreate(BaseModel):
    nome: Annotated[str, Field(min_length=3, max_length=150)]
    cpf: Annotated[str, Field(min_length=11, max_length=11)]

    @field_validator("nome", mode="before")
    @classmethod
    def normalizar_nome(cls, value: Any) -> str:

        if value is None:
            raise ValueError("Não deve ser Nulo")

        val_str = str(value).strip().lower()

        return val_str

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

        if re.match(r"^(\d)\1{10}$", cpf_limpo):
            raise ValueError("CPF inválido")

        return cpf_limpo


# ===================================================
# AlunoUpdate
# ===================================================
class AlunoUpdate(BaseModel):
    nome: NomeType | None = None
    cpf: NomeType | None = None

    @field_validator("nome", mode="before")
    @classmethod
    def normalizar_nome(cls, value: Any) -> str:

        if value is None:
            return None

        val_str = str(value).strip().lower()

        return val_str

    @field_validator("cpf", mode="before")
    @classmethod
    def normalizar_cpf(cls, value: Any) -> str:
        if value is None:
            raise None

        val_str = str(value).strip()

        # Remove casas decimais no final (ex: .0 ou .00 comuns vindas do Excel/Pandas)
        val_str = re.sub(r"\.0+$", "", val_str)

        # Remove tudo o que não for dígito (pontos, traços, letras, etc.)
        cpf_limpo = re.sub(r"\D", "", val_str)

        cpf_limpo = cpf_limpo.zfill(11)

        if len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos.")

        if re.match(r"^(\d)\1{10}$", cpf_limpo):
            raise ValueError("CPF inválido")

        return cpf_limpo


# ===================================================
# AlunoFiltro
# ===================================================
class AlunoFiltro(BaseModel):
    nome: str | None = Field(None, description="Filtrar por parte do nome")
    cpf: str | None = Field(None, description="Filtrar por parte do cpf")


# ===================================================
# AlunoResponse
# ===================================================
@dataclass
class VinculoResponse:
    id: str
    matricula: str
    email: str
    status: bool
    login: str
    senha: str
    is_primary: bool
    tags: str
    created_at: str
    updated_at: str


@dataclass
class AlunoResponse:
    id: str
    nome: str
    cpf: str
    vinculo: list[VinculoResponse]
    created_at: str
    updated_at: str


# ===================================================
# AlunoImportXlsx
# ===================================================
class AlunoImportXlsx(AlunoCreate):
    id: str | None = None
    isExist: bool | None = None


# ===================================================
# AlunoImportXlsxError
# ===================================================
@dataclass
class AlunoImportError:
    nome: str
    cpf: str
    detail: str | list

    def to_dict(self) -> dict:
        return asdict(self)
