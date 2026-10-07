from src.module.parametros.repository import Repository
from src.module.parametros.dto import ParametrosDto
from src.module.parametros.model import Parametros


class Service:
    def __init__(self):
        self.repository = Repository

    def create(self, paramDto: ParametrosDto) -> "Parametros":
        return self.repository.save(paramDto)

    def find_all(self) -> list["Parametros"]:
        return self.repository.find_all()

    def edit(self, id: int, paramDto: ParametrosDto) -> "Parametros":
        return self.repository.edit(id, paramDto)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
