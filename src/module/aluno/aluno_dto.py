from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field


class AlunoRequest(BaseModel):
    matricula: Annotated[str, Field(min_length=3, max_length=50)]
    nome: Annotated[str, Field(min_length=3, max_length=150)]
    codigo_externo: Annotated[str, Field(min_length=3, max_length=50)]
    cpf: Annotated[str, Field(min_length=11, max_length=11)]
    email: Annotated[str, Field(min_length=3, max_length=100)]
    login: Annotated[str, Field(min_length=3, max_length=100)]
    senha: Annotated[str, Field(min_length=3, max_length=100)]
    isAtivo: bool = False
