from src.module.parametros.repository import Repository
from src.module.parametros.dto import ParametrosDto
from src.module.parametros.model import Parametros


class Service:
    def __init__(self):
        self.repositori = Repository

    def create(self, paramDto: ParametrosDto) -> "Parametros":
        return self.repositori.save(paramDto)

    def find_all(self) -> list["Parametros"]:
        return self.repositori.find_all()

    def edit(self, id: int, paramDto: ParametrosDto) -> "Parametros":
        return self.repositori.edit(id, paramDto)

    def delete(self, id: int) -> bool:
        return self.repositori.delete(id)
