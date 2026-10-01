from pathlib import Path

from pydantic import BaseModel, field_validator
from enum import Enum
import pandas as pd


class TipoCategoria(str, Enum):
    ESTUDOS_DIRIGIDOS = "ESTUDOS_DIRIGIDOS"
    NORMAL = "NORMAL"
    OFICINA = "OFICINA"
    ORIENTACAO = "ORIENTACAO"
    PROFICIENCIA = "PROFICIENCIA"
    QUALIFICACAO = "QUALIFICACAO"
    SEMINARIO = "SEMINARIO"
    TCC = "TCC"
    ATIVIDADE_PROGRAMADA = "ATIVIDADE_PROGRAMADA"
    ATIVIDADES_DE_EXTENSAO = "ATIVIDADES_DE_EXTENSAO"
    DEFESA = "DEFESA"
    ESTAGIO = "ESTAGIO"


class CategoriasDisc(BaseModel):
    nome: str
    codigo: str
    tipo_categoria: TipoCategoria
    isAtiva: bool | str

    # =========================================
    # CREATER
    # =========================================
    @classmethod
    def read_excel(
        cls,
        file_path: Path,
        aba="1.3 Categorias Disc",
        colls={
            "nome": "Nome *",
            "codigo": "Código *",
            "tipo_categoria": "Tipo de Categoria *",
            "isAtiva": "Ativa? *",
        },
    ) -> list["CategoriasDisc"]:
        df = pd.read_excel(file_path, sheet_name=aba)

        box = []
        for _, v in df.iterrows():
            entity = cls(
                nome=v[colls["nome"]],
                codigo=v[colls["codigo"]],
                tipo_categoria=v[colls["tipo_categoria"]],
                isAtiva=v[colls["isAtiva"]],
            )
            box.append(entity)

        return box

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

    @field_validator("isAtiva")
    @classmethod
    def normalizar_isAtiva(cls, value: str | bool) -> bool:
        if isinstance(value, bool):
            return value

        if str(value).strip().lower() == "sim":
            return True

        return False
