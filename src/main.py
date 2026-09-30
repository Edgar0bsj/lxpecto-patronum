from pathlib import Path

from src.module.parametros.domain import Parametros
from src.module.modalidades.domain import Modalidades

from src.module.util.import_csv_entity import import_csv_entity


def main():

    file_path = Path("Planilha_Mestre.xlsx")

    CACHE = {}

    CACHE["Parametros"] = Parametros.read_excel(file_path)[0]
    CACHE["Modalidades"] = Modalidades.read_excel(file_path)

    import_csv_entity(CACHE, Modalidades)


if "__main__" == __name__:
    main()
