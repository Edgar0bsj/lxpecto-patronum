from pathlib import Path

from src.module.parametros.controller import ParametroController


def main():
    file_path = Path("Planilha_Mestre.xlsx")

    parametro = ParametroController()

    parametro.import_excel(file_path)


if "__main__" == __name__:
    main()
