from src.module.aluno.aluno_model import AlunoModel
from src.module.aluno.aluno_storage import AlunoStorage
from src.module.aluno.aluno_dto import AlunoFiltro, AlunoRequest
from src.module.aluno.aluno_dto import AlunoResponse, VinculoResponse
from nanoid import generate


class AlunoService:
    def __init__(self):
        self.repo = AlunoStorage()

    def gerar_id(self, prefixo: str = ""):
        token = generate(size=15)

        id = f"aluno_{prefixo}{token}"

        return id

    #
    #
    #
    #
    #
    #
    def save(self, aluno_dto: AlunoRequest):
        token = generate(size=10)
        id = f"aluno_{aluno_dto.cpf[-3:]}{token}"

        aluno = self.repo.create(id=id, aluno_dto=aluno_dto)

        return aluno

    #
    #
    #
    #
    #
    #
    def update_aluno(self, id: str, aluno_dto: AlunoRequest):
        return self.repo.update(id=id, aluno_model=aluno_dto)

    #
    #
    #
    #
    #
    #
    def find_all(self, aluno_filtro: AlunoFiltro) -> list[AlunoModel]:
        return self.repo.find_all(aluno_filtro)

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
    def find_by_cpf(self, cpf: str) -> AlunoModel:
        return self.repo.find_by_cpf(cpf)

    #
    #
    #
    #
    #
    #
    def parse_and_validate_rows(
        self,
        aluno_row: list[dict],
        col_nome="nome",
        col_cpf="cpf",
    ) -> tuple[list[AlunoRequest], list[dict]]:

        _buffer_alunos: list[AlunoRequest] = []
        _buffer_alunos_err: list[dict] = []

        for aluno in aluno_row:
            nome = aluno[col_nome]
            cpf = aluno[col_cpf]

            try:
                _buffer_alunos.append(AlunoRequest(nome=nome, cpf=cpf))

            except:
                _buffer_alunos_err.append(
                    {
                        "nome": nome,
                        "cpf": cpf,
                        "detalhes": "Error de validação",
                    }
                )
                continue

        return (_buffer_alunos, _buffer_alunos_err)

    #
    #
    #
    #
    #
    def mapper_lxp_manager(
        self,
        name: str,
        identityDocument: str,
        externalId: str,
        email: str,
        username: str,
        password: str,
        tags: str,
        isActive: bool,
    ):

        tag_parts = [item.strip() for item in tags.split(",") if item.strip()]
        tag_fmt = [f'["{item.upper()}"]' for item in tag_parts]
        tags_result = ",".join(tag_fmt)

        return {
            "name": name,
            "socialName": "",
            "identityDocument": identityDocument,
            "identityDocumentTypeId": "CPF",
            "passportNumber": "",
            "externalId": externalId,
            "address.zipCode": "",
            "address.state": "",
            "address.city": "",
            "address.address": "",
            "address.number": "",
            "address.neighborhood": "",
            "address.complement": "",
            "user.email": email,
            "user.username": username,
            "user.password": password,
            "tags": tags_result,
            "isActive": isActive,
        }

    # ===============================================
    # REFATORAÇÃO
    # ===============================================
    def isExist_cpf(self, cpf: str) -> bool:
        result = self.repo.find_by_cpf(cpf)

        if not result:
            return False

        return True

    #
    #
    #
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
        #
        #
        #

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
