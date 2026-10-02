from pydantic import BaseModel, field_validator, Field


class ParametrosDto(BaseModel):
    sigla_unidade: str = Field(..., min_length=3, max_length=7)
    nome_unidade: str = Field(..., min_length=3, max_length=25)
    isGPA: bool = Field(default=False)
    isNPJ: bool = Field(default=False)

    # =========================================
    # VALIDATORS
    # =========================================

    @field_validator("sigla_unidade")
    @classmethod
    def normalizar_sigla(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("nome_unidade")
    @classmethod
    def normalizar_nome(cls, value: str) -> str:
        return value.strip().lower()
