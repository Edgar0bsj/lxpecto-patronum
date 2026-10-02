from pathlib import Path
import pandas as pd

from src.module.parametros.repository import Repository
from src.module.parametros.dto import ParametrosDto
from src.database.database import create_database


class ParametroController:
    def __init__(self):
        create_database()

    @staticmethod
    def import_excel(
        file_path: Path, aba_name: str = "0.1 Parametros", coll: str = "Valor"
    ) -> bool:
        isExistElemento = True if len(Repository.find_all()) > 0 else False

        if isExistElemento:
            return False

        df = pd.read_excel(file_path, sheet_name=aba_name)

        _isGpa = False if str(df[coll][2]).strip().lower() != "sim" else True
        _isNpj = False if str(df[coll][3]).strip().lower() != "sim" else True

        _entity = ParametrosDto(
            sigla_unidade=str(df[coll][0]),
            nome_unidade=str(df[coll][1]),
            isGPA=_isGpa,
            isNPJ=_isNpj,
        )

        Repository.save(_entity)

        return True
