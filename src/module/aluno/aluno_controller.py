import io
from dataclasses import asdict

import pandas as pd
from fastapi import UploadFile
from pydantic import ValidationError

from src.module.aluno.aluno_dto import (
    AlunoCreate,
    AlunoFiltro,
    AlunoImportError,
    AlunoUpdate,
)
from src.module.aluno.aluno_model import AlunoModel
from src.module.aluno.aluno_service import AlunoService
from src.module.aluno.aluno_storage import AlunoStorage
from src.module.err.exceptions import ConflitoException, NotFoundException


class AlunoController:
    def __init__(self):
        self.service = AlunoService()
        self.repo = AlunoStorage()

    # ================================================================
    # ALUNO CREATED
    # ================================================================
    def aluno_created(self, aluno_created: AlunoCreate) -> None:

        isExist = self.repo.find_by_cpf(aluno_created.cpf)

        if isExist:
            raise ConflitoException("CPF já existe !")

        id = self.service.gerar_id()

        aluno = AlunoModel(id=id, nome=aluno_created.nome, cpf=aluno_created.cpf)

        self.repo.save(aluno)

    # ================================================================
    # ALUNO UPDATED
    # ================================================================
    def aluno_updated(self, id: str, aluno_updated: AlunoUpdate) -> None:
        aluno = self.repo.find_by_id(id)

        if not aluno:
            raise NotFoundException("Id não encontrado!")

        if aluno_updated.cpf and aluno_updated.cpf != aluno.cpf:
            isExist_cpf = self.repo.find_by_cpf(aluno_updated.cpf)

            if isExist_cpf:
                raise ConflitoException("CPF Já Cadastrado !")

        if aluno_updated.nome:
            aluno.nome = aluno_updated.nome
        if aluno_updated.cpf:
            aluno.cpf = aluno_updated.cpf

        self.repo.update(id, aluno)

    # ================================================================
    # ALUNO GET ALL
    # ================================================================
    def aluno_get_all(self, aluno_filtro: AlunoFiltro):
        alunos = self.repo.find_all(aluno_filtro)

        if len(alunos) == 0:
            return []

        result = self.service.model_to_response(alunos)

        res = [asdict(el) for el in result]

        return res

    # ================================================================
    # ALUNO DELETE
    # ================================================================
    def aluno_delete(self, id: str) -> None:
        result = self.repo.delete(id)

        if not result:
            raise NotFoundException("Id não encontrado !")

    # ================================================================
    # ALUNO FIND BY NOME
    # ================================================================
    def find_by_nome(self, nome: str):
        return self.service.find_by_nome(nome)

    # ================================================================
    # ALUNO IMPORT XLSX
    # ================================================================
    async def aluno_import_xlsx(self, file: UploadFile):

        if not file.filename or not file.filename.endswith(".xlsx"):
            raise ValueError("Apenas arquivos no formato .xlsx são permitidos")

        contents = await file.read()

        alunos_impot_dto, alunos_impot_errs = self.service.convert_to_import_DTO(
            contents=contents
        )

        for elun in alunos_impot_dto:
            cpf_exist = self.repo.find_by_cpf(elun.cpf)
            elun.isExist = bool(cpf_exist)
            elun.id = cpf_exist.id if bool(cpf_exist) else None

        alunos_created = [el for el in alunos_impot_dto if not el.isExist]
        alunos_updated = [el for el in alunos_impot_dto if el.isExist]

        for add in alunos_created:
            try:
                self.aluno_created(AlunoCreate(nome=add.nome, cpf=add.cpf))
            except ValidationError as err:
                alunos_impot_errs.append(
                    AlunoImportError(nome=add.nome, cpf=add.cpf, detail=err.errors())
                )
            except ConflitoException as err:
                alunos_impot_errs.append(
                    AlunoImportError(nome=add.nome, cpf=add.cpf, detail=err.detail)
                )

        for updat in alunos_updated:
            try:
                self.aluno_updated(
                    id=updat.id,
                    aluno_updated=AlunoUpdate(nome=updat.nome, cpf=updat.cpf),
                )
            except ValidationError as err:
                alunos_impot_errs.append(
                    AlunoImportError(
                        nome=updat.nome, cpf=updat.cpf, detail=err.errors()
                    )
                )
            except ConflitoException as err:
                alunos_impot_errs.append(
                    AlunoImportError(nome=updat.nome, cpf=updat.cpf, detail=err.detail)
                )

        _temp_df = pd.DataFrame(alunos_impot_errs)
        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            _temp_df.to_excel(writer, index=False, sheet_name="alunos_err")

        excel_buffer.seek(0)

        def iterfile():
            yield excel_buffer.getvalue()

        return iterfile

    # ================================================================
    # ALUNO EXCEL TAMPLETE
    # ================================================================
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
