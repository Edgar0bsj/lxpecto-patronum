from src.module.vinculo.vinculo_service import VinculoService
from src.module.vinculo.vinculo_dto import VinculoDto, VinculoFiltro


class VinculoController:
    def __init__(self):
        self.service = VinculoService()

    def create_vinculo(self, vinculo_dto: VinculoDto):
        result = self.service.create_vinculo(vinculo_dto)

        return result.__dict__

    #
    #
    #
    #
    #
    def update_vinculo(self, id: str, vinculo_dto: VinculoDto):
        result = self.service.update_vinculo(id, vinculo_dto)
        return result.__dict__

    #
    #
    #
    #
    #
    def find_all_vinculo(self, vinculo_filtro: VinculoFiltro):
        result = self.service.find_all(vinculo_filtro)

        if len(result) == 0:
            return []

        alunos = [el.__dict__ for el in result]
        return alunos

    #
    #
    #
    #
    #
    def delete_vinculo(self, id: str):
        return self.service.delete(id)
