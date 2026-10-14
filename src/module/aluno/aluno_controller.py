from src.module.aluno.aluno_service import AlunoService
from src.module.aluno.aluno_dto import AlunoRequest, AlunoFiltro


class AlunoController:
    def __init__(self):
        self.service = AlunoService()

    def create_aluno(self, aluno_dto: AlunoRequest):
        result = self.service.create_aluno(aluno_dto)

        return result.__dict__

    #
    #
    #
    #
    #
    def update_aluno(self, id: str, aluno_dto: AlunoRequest):
        result = self.service.update_aluno(id, aluno_dto)
        return result.__dict__

    #
    #
    #
    #
    #
    def find_all_aluno(self, aluno_filtro: AlunoFiltro):
        result = self.service.find_all(aluno_filtro)

        if len(result) == 0:
            return []

        alunos = [el.__dict__ for el in result]
        return alunos

    #
    #
    #
    #
    #
    def delete_aluno(self, id: str):
        return self.service.delete(id)

    #
    #
    #
    #
    #
    def find_by_nome(self, nome: str):
        return self.service.find_by_nome(nome)
