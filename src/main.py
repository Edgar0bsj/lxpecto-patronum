from pathlib import Path

from src.module.parametros.domain import Parametros
from src.module.modalidades.domain import Modalidades
from src.module.niveis_ensino.domain import NivelEnsino
from src.module.categorias_disc.domain import CategoriasDisc


def main():

    file_path = Path("Planilha_Mestre.xlsx")

    CACHE = {}

    CACHE["Parametros"] = Parametros.read_excel(file_path)
    CACHE["Modalidades"] = Modalidades.read_excel(file_path)
    CACHE["NivelEnsino"] = NivelEnsino.read_excel(file_path)
    CACHE["CategoriasDisc"] = CategoriasDisc.read_excel(file_path)


if "__main__" == __name__:
    main()
