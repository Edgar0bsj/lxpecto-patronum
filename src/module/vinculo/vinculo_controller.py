from src.module.vinculo.vinculo_service import VinculoService
from src.module.vinculo.vinculo_dto import VinculoDto, VinculoFiltro
from src.module.aluno.aluno_service import AlunoService


class VinculoController:
    def __init__(self):
        self.service = VinculoService()
        self.service_aluno = AlunoService()

    def create_vinculo(self, vinculo_dto: VinculoDto):
        aluno = self.service_aluno.find_by_id(vinculo_dto.aluno_id)

        if not aluno:
            raise ValueError("Aluno não existe na base de dados")

        vinculos = self.service.find_all(
            VinculoFiltro(aluno_id=vinculo_dto.aluno_id, is_primary=True)
        )

        if len(vinculos) != 0:
            vinculo_dto.is_primary = False
        else:
            vinculo_dto.is_primary = True

        result = self.service.create_vinculo(vinculo_dto)

        return result.__dict__

    #
    #
    #
    #
    #
    def update_vinculo(self, id: str, vinculo_dto: VinculoDto):
        aluno = self.service_aluno.find_by_id(vinculo_dto.aluno_id)

        if not aluno:
            raise ValueError("Aluno não existe na base de dados")

        if vinculo_dto.is_primary:
            vinculos = self.service.find_all(
                VinculoFiltro(aluno_id=vinculo_dto.aluno_id, is_primary=True)
            )

            if len(vinculos) != 0:
                for vinc in vinculos:
                    vinc_dto = VinculoDto(
                        matricula=vinc.matricula,
                        email=vinc.email,
                        status=vinc.status,
                        login=vinc.login,
                        senha=vinc.senha,
                        is_primary=False,
                        aluno_id=vinc.aluno_id,
                    )
                    self.service.update_vinculo(vinc.id, vinc_dto)
        #
        #
        #

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
