from src.module.aluno.aluno_service import AlunoService
from src.module.err.exceptions import ConflitoException, NotFoundException
from src.module.vinculo.vinculo_dto import VinculoCreatedDto
from src.module.vinculo.vinculo_model import VinculoModel
from src.module.vinculo.vinculo_service import VinculoService
from src.module.vinculo.vinculo_storage import VinculoStorage


class VinculoController:
    def __init__(self):
        self.svc = VinculoService()
        self.repo = VinculoStorage()
        self.aluno_svc = AlunoService()

    # ===============================================
    # VINCULO CREATED
    # ===============================================
    def vinculo_created(self, vinculo_dto: VinculoCreatedDto):

        aluno = self.aluno_svc.repo.find_by_cpf(vinculo_dto.aluno_cpf)

        if not aluno:
            raise NotFoundException("Aluno não encontrado!")

        isExist_matricula = self.repo.is_exist(matricula=vinculo_dto.matricula)
        isExist_email = self.repo.is_exist(email=vinculo_dto.email)
        isExist_login = self.repo.is_exist(login=vinculo_dto.login)

        if isExist_matricula or isExist_email or isExist_login:
            raise ConflitoException("Conflito de dados")

        is_primary = None
        if len(aluno.vinculo) != 0:
            is_primary = False
        else:
            is_primary = True

        id = self.svc.generate_id()

        vinculo_model = VinculoModel(
            id=id,
            matricula=vinculo_dto.matricula,
            email=vinculo_dto.email,
            status=vinculo_dto.status,
            login=vinculo_dto.login,
            senha=vinculo_dto.senha,
            is_primary=is_primary,
            tags=vinculo_dto.tags,
            aluno_id=aluno.id,
        )

        self.repo.save(vinculo_model)
