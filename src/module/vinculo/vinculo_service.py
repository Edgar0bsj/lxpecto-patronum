from src.module.vinculo.vinculo_model import VinculoModel
from src.module.vinculo.vinculo_storage import VinculoStorage
from src.module.vinculo.vinculo_dto import VinculoDto, VinculoFiltro
from src.module.aluno.aluno_storage import AlunoStorage

from nanoid import generate


class VinculoService:
    def __init__(self):
        self.repo = VinculoStorage()
        self.aluno_repo = AlunoStorage()

    #
    #
    #
    #
    #
    #
    def create_vinculo(self, vinculo_dto: VinculoDto):
        token = generate(size=10)
        id = f"vinc_{vinculo_dto.matricula[-3:]}{token}"

        aluno = self.repo.create(id, vinculo_dto)

        return aluno

    #
    #
    #
    #
    #
    #
    def update_vinculo(self, id: str, vinculo_dto: VinculoDto):
        return self.repo.update(id=id, vinculo_dto=vinculo_dto)

    #
    #
    #
    #
    #
    #
    def find_all(self, vinculo_filtro: VinculoFiltro) -> list["VinculoModel"]:
        return self.repo.find_all(vinculo_filtro)

    #
    #
    #
    #
    #
    #
    def delete(self, id: str) -> bool:
        return self.repo.delete(id)

    #
    #
    #
    #
    #
    #
    def find_by_id(self, id: str) -> "VinculoModel":
        return self.repo.find_by_id(id)
