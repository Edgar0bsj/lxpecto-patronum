from src.module.aluno.aluno_service import AlunoService
from fastapi import HTTPException

from src.module.aluno.aluno_dto import AlunoRequest


class AlunoController:
    def __init__(self):
        self.service = AlunoService()

    def create_aluno(self, aluno_dto: AlunoRequest):
        return self.service.create_aluno(aluno_dto)
