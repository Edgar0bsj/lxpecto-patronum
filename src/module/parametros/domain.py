from pathlib import Path

from pydantic import BaseModel, field_validator
import pandas as pd


class Parametros(BaseModel):
    sigla_unidade: str
    nome_unidade: str
    isGPA: bool | str = False
    isNPJ: bool | str = False

    # =========================================
    # CREATER
    # =========================================
    @classmethod
    def read_excel(
        cls, file_path: Path, aba="0.1 Parametros", colls={"valor": "Valor"}
    ) -> list["Parametros"]:
        result = pd.read_excel(file_path, sheet_name=aba)

        result = result[colls["valor"]]

        return cls(
            sigla_unidade=result[0],
            nome_unidade=result[1],
            isGPA=result[2],
            isNPJ=result[3],
        )

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

    @field_validator("isGPA")
    @classmethod
    def normalizar_isGPA(cls, value: str) -> str:

        if value.lower() == "sim":
            return True

        return False

    @field_validator("isNPJ")
    @classmethod
    def normalizar_isNPJ(cls, value: str) -> str:

        if value.lower() == "sim":
            return True

        return False
