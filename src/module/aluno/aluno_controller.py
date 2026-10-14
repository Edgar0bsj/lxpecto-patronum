import io

from src.module.aluno.aluno_service import AlunoService
from src.module.aluno.aluno_dto import AlunoRequest, AlunoFiltro

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
import pandas as pd


class AlunoController:
    def __init__(self):
        self.service = AlunoService()

    def create_aluno(self, aluno_dto: AlunoRequest):
        result = self.service.create_aluno(aluno_dto)

        return result.__dict__

    #
    #
    #
    #
    #
    def update_aluno(self, id: str, aluno_dto: AlunoRequest):
        result = self.service.update_aluno(id, aluno_dto)
        return result.__dict__

    #
    #
    #
    #
    #
    def find_all_aluno(self, aluno_filtro: AlunoFiltro):
        result = self.service.find_all(aluno_filtro)

        if len(result) == 0:
            return []

        alunos = [el.__dict__ for el in result]
        return alunos

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
            raise ValueError("Apenas arquivos no formato .xlsx são permitidos.")

        contents = await file.read()

        df = pd.read_excel(io.BytesIO(contents))

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
                self.create_aluno(add_aluno)
            except IntegrityError as err:
                alunos_err.append(
                    {
                        "nome": add_aluno.nome,
                        "cpf": add_aluno.cpf,
                        "login": add_aluno.login,
                        "senha": add_aluno.senha,
                        "detalhes": str(err.orig),
                    }
                )
                continue

        for update_aluno in alunos_exist:
            try:
                self.update_aluno(update_aluno["id"], update_aluno["aluno"])
            except IntegrityError as err:
                alunos_err.append(
                    {
                        "nome": update_aluno["aluno"].nome,
                        "cpf": update_aluno["aluno"].cpf,
                        "login": update_aluno["aluno"].login,
                        "senha": update_aluno["aluno"].senha,
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
        _tamplete = {
            "nome": "",
            "cpf": "",
            "login": "",
            "senha": "",
        }
        df = pd.DataFrame(_tamplete)
        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="tamplete")

        excel_buffer.seek(0)

        def iterfile():
            yield excel_buffer.getvalue()

        return iterfile
