import io

from fastapi import UploadFile
import pandas as pd
from sqlalchemy.exc import IntegrityError

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

        vinculo_dto.is_primary = self.service.garantir_vinculo_primario_unico(
            vinculo_dto=vinculo_dto, is_primary=True
        )

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

        vinculo_dto.is_primary = self.service.garantir_vinculo_primario_unico(
            vinculo_dto=vinculo_dto, is_primary=vinculo_dto.is_primary
        )

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

    #
    #
    #
    #
    #
    async def export_excel_tamplete(self):
        _tamplete = [
            {
                "cpf_aluno": "",
                "matricula": "",
                "email": "",
                "status": "",
                "login": "",
                "senha": "",
                "is_primary": "",
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
    #
    async def import_excel_vinculo(self, file: UploadFile):

        if not file.filename or not file.filename.endswith(".xlsx"):
            raise ValueError("Apenas arquivos no formato .xlsx são permitidos.")

        contents = await file.read()

        df = pd.read_excel(io.BytesIO(contents))

        df = df.fillna("")

        dados_alunos = df.to_dict(orient="records")

        vinculos, vinculos_err = self.service.parse_and_validate_rows(dados_alunos)

        # ===

        vinculos_exist: list[tuple[str, VinculoDto]] = []
        vinculos_notExist: list[VinculoDto] = []

        for cpf_aluno, vinc_dto in vinculos:
            self.service.validar_e_separar_vinculos(
                service_aluno=self.service_aluno,
                cpf_aluno=cpf_aluno,
                vinc_dto=vinc_dto,
                buffer_err=vinculos_err,
                buffer_exist=vinculos_exist,
                buffer_notExist=vinculos_notExist,
            )
        # ====

        for add_vinc in vinculos_notExist:
            try:
                self.create_vinculo(add_vinc)
            except IntegrityError as err:
                vinculos_err.append(
                    {
                        "cpf_aluno": "",
                        "matricula": add_vinc.matricula,
                        "email": add_vinc.email,
                        "status": add_vinc.status,
                        "login": add_vinc.login,
                        "senha": add_vinc.senha,
                        "is_primary": add_vinc.is_primary,
                        "detalhes": str(err.detail),
                    }
                )

        for vinc_id, upd_vinc in vinculos_exist:
            try:
                self.update_vinculo(vinc_id, upd_vinc)
            except IntegrityError as err:
                vinculos_err.append(
                    {
                        "cpf_aluno": "",
                        "matricula": upd_vinc.matricula,
                        "email": upd_vinc.email,
                        "status": upd_vinc.status,
                        "login": upd_vinc.login,
                        "senha": upd_vinc.senha,
                        "is_primary": upd_vinc.is_primary,
                        "detalhes": str(err.detail),
                    }
                )

        # ======

        _temp_df = pd.DataFrame(vinculos_err)
        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            _temp_df.to_excel(writer, index=False, sheet_name="alunos_err")

        excel_buffer.seek(0)

        def iterfile():
            yield excel_buffer.getvalue()

        return iterfile
