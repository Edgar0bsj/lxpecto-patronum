from dataclasses import asdict
import io

from src.module.err.exceptions import ConflitoException, NotFoundException

from src.module.aluno.aluno_model import AlunoModel
from src.module.aluno.aluno_storage import AlunoStorage

from src.module.aluno.aluno_service import AlunoService
from src.module.aluno.aluno_dto import AlunoRequest, AlunoFiltro
from src.module.aluno.aluno_dto import AlunoCreate, AlunoUpdate

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
import pandas as pd


class AlunoController:
    def __init__(self):
        self.service = AlunoService()
        self.repo = AlunoStorage()

    def aluno_created(self, aluno_created: AlunoCreate) -> None:

        isExist = self.service.isExist_cpf(aluno_created.cpf)

        if isExist:
            raise ConflitoException("CPF já existe !")

        id = self.service.gerar_id()

        aluno = AlunoModel(id=id, nome=aluno_created.nome, cpf=aluno_created.cpf)

        self.repo.save(aluno)

        return None

    #
    #
    #
    #
    #
    def aluno_updated(self, id: str, aluno_updated: AlunoUpdate) -> None:
        aluno = self.repo.find_by_id(id)

        if not aluno:
            raise NotFoundException("Id não encontrado!")

        if aluno_updated.cpf and aluno_updated.cpf != aluno.cpf:
            isExist_cpf = self.service.isExist_cpf(aluno_updated.cpf)

            if isExist_cpf:
                raise ConflitoException("CPF já cadastrado !")

        if aluno_updated.nome:
            aluno.nome = aluno_updated.nome
        if aluno_updated.cpf:
            aluno.cpf = aluno_updated.cpf

        self.repo.update(id, aluno)

    #
    #
    #
    #
    #
    def aluno_get_all(self, aluno_filtro: AlunoFiltro):
        alunos = self.repo.find_all(aluno_filtro)

        if len(alunos) == 0:
            return []

        result = self.service.model_to_response(alunos)

        res = [asdict(el) for el in result]

        return res

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

    #
    #
    #
    #
    #
    async def import_excel_aluno(self, file: UploadFile):

        if not file.filename or not file.filename.endswith(".xlsx"):
            raise ValueError("Apenas arquivos no formato .xlsx são permitidos")

        contents = await file.read()

        df = pd.read_excel(io.BytesIO(contents))

        df = df.fillna("")

        dados_alunos = df.to_dict(orient="records")

        alunos, alunos_err = self.service.parse_and_validate_rows(dados_alunos)

        # ===

        alunos_exist: list = []
        alunos_notExist: list[AlunoRequest] = []

        for elem in alunos:
            isExist = self.service.find_by_cpf(elem.cpf)

            if not isExist:
                alunos_notExist.append(elem)
                continue

            alunos_exist.append({"id": isExist.id, "aluno": elem})
            continue

        # ====

        for add_aluno in alunos_notExist:
            try:
                self.aluno_created(add_aluno)
            except IntegrityError as err:
                alunos_err.append(
                    {
                        "nome": add_aluno.nome,
                        "cpf": add_aluno.cpf,
                        "detalhes": str(err.orig),
                    }
                )
                continue

        for update_aluno in alunos_exist:
            try:
                self.aluno_updated(update_aluno["id"], update_aluno["aluno"])
            except IntegrityError as err:
                alunos_err.append(
                    {
                        "nome": update_aluno["aluno"].nome,
                        "cpf": update_aluno["aluno"].cpf,
                        "detalhes": str(err.orig),
                    }
                )
                continue

        # ======

        _temp_df = pd.DataFrame(alunos_err)
        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            _temp_df.to_excel(writer, index=False, sheet_name="alunos_err")

        excel_buffer.seek(0)

        def iterfile():
            yield excel_buffer.getvalue()

        return iterfile

    #
    #
    #
    #
    #
    async def export_excel_tamplete(self):
        _tamplete = [
            {
                "nome": "",
                "cpf": "",
            }
        ]
        df = pd.DataFrame(_tamplete)
        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="tamplete")

        excel_buffer.seek(0)

        def iterfile():
            yield excel_buffer.getvalue()

        return iterfile

    #
    #
    #
    #
    async def export_lxp_manager(self):

        alunos = self.service.find_all(AlunoFiltro())

        _person_buffer = []
        for alun in alunos:
            vinculos = alun.vinculo
            vinculo_ativo = next((e for e in vinculos if e.is_primary), None)

            if vinculo_ativo is None:
                continue

            tags = vinculo_ativo.tags
            person_xlp = self.service.mapper_lxp_manager(
                name=alun.nome.title(),
                identityDocument=alun.cpf,
                externalId=alun.cpf,
                email=vinculo_ativo.email,
                username=vinculo_ativo.login,
                password=vinculo_ativo.senha,
                tags=tags,
                isActive=vinculo_ativo.status,
            )

            _person_buffer.append(person_xlp)

        df = pd.DataFrame(_person_buffer)

        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False, sep=";", encoding="utf-8")

        csv_buffer.seek(0)

        def iterfile():
            yield csv_buffer.getvalue()

        return iterfile
