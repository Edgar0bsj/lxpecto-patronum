from src.module.aluno.aluno_model import AlunoModel
from src.module.aluno.aluno_storage import AlunoStorage
from src.module.aluno.aluno_dto import AlunoRequest
from nanoid import generate


class AlunoService:
    def __init__(self):
        self.repo = AlunoStorage()

    #
    #
    #
    #
    #
    #
    def create_aluno(self, aluno_dto: AlunoRequest):
        token = generate(size=10)
        id = f"aluno_{token}"

        aluno = self.repo.create(
            id=id,
            matricula=aluno_dto.matricula,
            nome=aluno_dto.nome,
            codigo_externo=aluno_dto.codigo_externo,
            cpf=aluno_dto.cpf,
            email=aluno_dto.email,
            login=aluno_dto.login,
            senha=aluno_dto.senha,
            isAtivo=aluno_dto.isAtivo,
        )

        return aluno

    #
    #
    #
    #
    #
    #
    def update_aluno(self, id: str, aluno_dto: AlunoRequest):
        return self.repo.update(
            id=id,
            matricula=aluno_dto.matricula,
            nome=aluno_dto.nome,
            codigo_externo=aluno_dto.codigo_externo,
            cpf=aluno_dto.cpf,
            email=aluno_dto.email,
            login=aluno_dto.login,
            senha=aluno_dto.senha,
            isAtivo=aluno_dto.isAtivo,
        )

    #
    #
    #
    #
    #
    #
    def find_all(self) -> list[AlunoModel]:
        return self.repo.find_all()

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
    def find_by_id(self, id: str) -> AlunoModel:
        return self.repo.find_by_id(id)

    #
    #
    #
    #
    #
    #
    def find_by_cod_externo(self, codigo_externo: str) -> AlunoModel:
        return self.repo.find_by_cod_externo(codigo_externo)
