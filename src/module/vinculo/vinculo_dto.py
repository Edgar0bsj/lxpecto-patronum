import re
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_validator

MatriculaType = Annotated[str, Field(min_length=3, max_length=100)]
EmailType = Annotated[str, Field(min_length=3, max_length=100)]
StatusType = bool
LoginType = Annotated[str, Field(min_length=3, max_length=100)]
SenhaType = Annotated[str, Field(min_length=3, max_length=100)]
TagsType = Annotated[str, Field(min_length=3, max_length=150)]
AlunoCPFType = Annotated[str, Field(min_length=3, max_length=100)]
# AlunoIdType = Annotated[str, Field(min_length=3, max_length=100)]


# ===================================================
# VINCULO CREATED
# ===================================================
class VinculoCreatedDto(BaseModel):
    matricula: MatriculaType
    email: EmailType
    status: StatusType
    login: LoginType
    senha: SenhaType
    tags: TagsType | None = None
    aluno_cpf: AlunoCPFType

    # -------------------------------------------------------
    # FILD VALIDATOR - MATRICULA
    # -------------------------------------------------------
    @field_validator("matricula", mode="before")
    @classmethod
    def normalizar_matricula(cls, value: Any) -> str:
        if not value:
            return value

        val_str = str(value).strip()

        val_str = re.sub(r"\.0+$", "", val_str)

        return val_str

    # -------------------------------------------------------
    # FILD VALIDATOR - EMAIL
    # -------------------------------------------------------
    @field_validator("email", mode="before")
    @classmethod
    def normalizar_email(cls, value: Any) -> str:
        if not value:
            return value

        val_str = str(value).strip()

        email_limpo = val_str.lower()

        regex_email = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"

        if not re.match(regex_email, email_limpo):
            raise ValueError("O e-mail informado possui um formato inválido.")

        return email_limpo

    # -------------------------------------------------------
    # FILD VALIDATOR - LOGIN
    # -------------------------------------------------------
    @field_validator("login", mode="before")
    @classmethod
    def normalizar_login(cls, value: Any) -> str:
        if not value:
            return value

        val_str = str(value).strip()

        val_str = re.sub(r"\.0+$", "", val_str)

        return val_str

    # -------------------------------------------------------
    # FILD VALIDATOR - SENHA
    # -------------------------------------------------------
    @field_validator("senha", mode="before")
    @classmethod
    def normalizar_senha(cls, value: Any) -> str:
        return value

    # -------------------------------------------------------
    # FILD VALIDATOR - TAGS
    # -------------------------------------------------------
    @field_validator("tags", mode="before")
    @classmethod
    def normalizar_tags(cls, value: Any) -> str:
        if not value:
            return ""

        texto_bruto = str(value).strip()
        partes = [item.strip() for item in texto_bruto.split(",") if item.strip()]

        val_str = ", ".join(partes)
        return val_str


# ===================================================
# Vinculo FILTRO
# ===================================================
class VinculoFiltro(BaseModel):
    matricula: str | None = Field(None, description="Filtrar por parte do matricula")
    email: str | None = Field(None, description="Filtrar por parte do email")
    status: bool | None = Field(None, description="Filtrar por status")
    login: str | None = Field(None, description="Filtrar por parte do login")
    is_primary: bool | None = Field(None, description="Filtrar por is_primary")
    aluno_id: str | None = Field(None, description="Filtrar por aluno_id")
    tags: str | None = Field(None, description="Filtrar por tags")
