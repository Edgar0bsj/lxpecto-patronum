import io

import pandas as pd
from nanoid import generate
from pydantic import ValidationError

from src.module.aluno.aluno_dto import (
    AlunoImportError,
    AlunoImportXlsx,
    AlunoResponse,
    VinculoResponse,
)
from src.module.aluno.aluno_model import AlunoModel
from src.module.aluno.aluno_storage import AlunoStorage


class AlunoService:
    def __init__(self):
        self.repo = AlunoStorage()

    # =============================================
    # Gerar Id
    # =============================================
    def gerar_id(self, prefixo: str = ""):
        token = generate(size=15)

        id = f"aluno_{prefixo}{token}"

        return id

    # =============================================
    # Find By Id
    # =============================================
    def find_by_id(self, id: str) -> AlunoModel:
        return self.repo.find_by_id(id)

    # ===============================================
    # Model Aluno Para Response Aluno
    # ===============================================
    def model_to_response(
        self, aluno_model: list[AlunoModel] | AlunoModel
    ) -> list[AlunoResponse] | AlunoResponse:
        if isinstance(aluno_model, list):
            _buffer: list[AlunoResponse] = []
            for aluno in aluno_model:

                _alun = AlunoResponse(
                    id=aluno.id,
                    nome=aluno.nome,
                    cpf=aluno.cpf,
                    vinculo=[],
                    created_at=str(aluno.created_at),
                    updated_at=str(aluno.updated_at),
                )

                if len(aluno.vinculo) == 0:
                    _buffer.append(_alun)
                    continue

                for vinc in aluno.vinculo:
                    _vinculo = VinculoResponse(
                        id=vinc.id,
                        matricula=vinc.matricula,
                        email=vinc.email,
                        status=vinc.status,
                        login=vinc.login,
                        senha=vinc.senha,
                        is_primary=vinc.is_primary,
                        tags=vinc.tags,
                        created_at=str(vinc.created_at),
                        updated_at=str(vinc.updated_at),
                    )
                    _alun.vinculo.append(_vinculo)

                _buffer.append(_alun)

            return _buffer

        _alun = AlunoResponse(
            id=aluno_model.id,
            nome=aluno_model.nome,
            cpf=aluno_model.cpf,
            vinculo=[],
            created_at=aluno_model.created_at,
            updated_at=aluno_model.updated_at,
        )

        if len(aluno_model.vinculo) == 0:
            return _alun

        for vinc in _alun.vinculo:
            _vinculo = VinculoResponse(
                id=vinc.id,
                matricula=vinc.matricula,
                email=vinc.email,
                status=vinc.status,
                login=vinc.login,
                senha=vinc.senha,
                is_primary=vinc.is_primary,
                tags=vinc.tags,
                created_at=vinc.created_at,
                updated_at=vinc.updated_at,
            )
            _alun.vinculo.append(_vinculo)

        return _alun

    # =============================================
    # Convertendo De Xlsx Para DTO De Import
    # =============================================
    def convert_to_import_DTO(
        self, contents: bytes, collum=["nome", "cpf"]
    ) -> tuple[list["AlunoImportXlsx"], list["AlunoImportError"]]:

        df = pd.read_excel(io.BytesIO(contents))

        df.fillna("")

        alunos_dict = df.to_dict(orient="records")

        _buffer_alunos = []
        _buffer_erros = []

        for aluno in alunos_dict:
            _nome = aluno[collum[0]]
            _cpf = aluno[collum[1]]

            try:
                _element = AlunoImportXlsx(nome=_nome, cpf=_cpf)
                _buffer_alunos.append(_element)

            except ValidationError as err:
                _buffer_erros.append(
                    AlunoImportError(nome=_nome, cpf=_cpf, detail=str(err))
                )

        return (_buffer_alunos, _buffer_erros)
