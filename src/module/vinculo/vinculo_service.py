import re
from typing import Any

from src.module.vinculo.vinculo_model import VinculoModel
from src.module.vinculo.vinculo_storage import VinculoStorage
from src.module.vinculo.vinculo_dto import VinculoDto, VinculoFiltro

from nanoid import generate


class VinculoService:
    def __init__(self):
        self.repo = VinculoStorage()

    #
    #
    #
    #
    #
    #
    def create_vinculo(self, vinculo_dto: VinculoDto):

        token = generate(size=10)
        id = f"vinc_{vinculo_dto.matricula[-3:]}{token}"

        vinculos = self.find_all(
            VinculoFiltro(aluno_id=vinculo_dto.aluno_id, is_primary=True)
        )

        if len(vinculos) != 0:
            vinculo_dto.is_primary = False

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

    #
    #
    #
    #
    #
    #
    def parse_and_validate_rows(
        self,
        vinculo_row: list[dict],
        col_cpf_aluno="cpf_aluno",
        col_matricula="matricula",
        col_email="email",
        col_status="status",
        col_login="login",
        col_senha="senha",
        col_is_primary="is_primary",
        col_tags="tags",
    ) -> tuple[list[tuple[str, VinculoDto]], list[dict]]:

        _buffer_vinculo: list[tuple] = []
        _buffer_vinculo_err: list[dict] = []

        for vinc in vinculo_row:
            cpf_aluno = vinc[col_cpf_aluno]
            matricula = vinc[col_matricula]
            email = vinc[col_email]
            status = vinc[col_status]
            login = vinc[col_login]
            senha = vinc[col_senha]
            tags = vinc[col_tags]

            is_primary = True
            if "is_primary" in vinc:
                is_primary = vinc[col_is_primary]

            try:
                _buffer_vinculo.append(
                    (
                        str(cpf_aluno),
                        VinculoDto(
                            matricula=matricula,
                            email=email,
                            status=status,
                            login=login,
                            senha=senha,
                            is_primary=is_primary,
                            aluno_id=None,
                            tags=tags,
                        ),
                    )
                )

            except:
                _buffer_vinculo_err.append(
                    {
                        "cpf_aluno": cpf_aluno,
                        "matricula": matricula,
                        "email": email,
                        "status": status,
                        "login": login,
                        "senha": senha,
                        "is_primary": is_primary,
                        "tags": tags,
                        "detalhes": "Error de validação",
                    }
                )
                continue

        return (_buffer_vinculo, _buffer_vinculo_err)

    #
    #
    #
    def validar_e_separar_vinculos(
        self,
        service_aluno: Any,
        cpf_aluno: str,
        vinc_dto: VinculoDto,
        buffer_err: list,
        buffer_exist: list,
        buffer_notExist: list,
    ):
        vinculo_isExist = self.find_all(VinculoFiltro(matricula=vinc_dto.matricula))

        cpf_valor = str(cpf_aluno).strip()

        cpf_valor = re.sub(r"\.0+$", "", cpf_valor)
        cpf_limpo = re.sub(r"\D", "", cpf_valor)
        cpf_limpo = cpf_limpo.zfill(11)

        if len(cpf_limpo) != 11:
            buffer_err.append(
                {
                    "cpf_aluno": cpf_aluno,
                    "matricula": vinc_dto.matricula,
                    "email": vinc_dto.email,
                    "status": vinc_dto.status,
                    "login": vinc_dto.login,
                    "senha": vinc_dto.senha,
                    "is_primary": vinc_dto.is_primary,
                    "tags": vinc_dto.tags,
                    "detalhes": "O CPF deve conter exatamente 11 dígitos",
                }
            )
            return

        aluno = service_aluno.find_by_cpf(cpf_limpo)

        if not aluno:
            buffer_err.append(
                {
                    "cpf_aluno": cpf_limpo,
                    "matricula": vinc_dto.matricula,
                    "email": vinc_dto.email,
                    "status": vinc_dto.status,
                    "login": vinc_dto.login,
                    "senha": vinc_dto.senha,
                    "is_primary": vinc_dto.is_primary,
                    "tags": vinc_dto.tags,
                    "detalhes": "cpf não existe na base de dados",
                }
            )
            return

        vinc_dto.aluno_id = aluno.id

        if len(vinculo_isExist) == 0:
            buffer_notExist.append(vinc_dto)
            return

        buffer_exist.append((vinculo_isExist[0].id, vinc_dto))
        return

    #
    #
    #
    def garantir_vinculo_primario_unico(
        self, vinculo_dto: VinculoDto, is_primary: bool
    ):

        vinculos = self.find_all(
            VinculoFiltro(aluno_id=vinculo_dto.aluno_id, is_primary=True)
        )

        if is_primary and len(vinculos) != 0:

            for vinc in vinculos:
                vinc_dto = VinculoDto(
                    matricula=vinc.matricula,
                    email=vinc.email,
                    status=vinc.status,
                    login=vinc.login,
                    senha=vinc.senha,
                    is_primary=False,
                    aluno_id=vinc.aluno_id,
                    tags=vinc.tags,
                )
                self.update_vinculo(vinc.id, vinc_dto)

        return True
