from src.database.database import create_database
from src.cli.prompts import (
    parametros_menu_prompt,
    edit_parametros_form,
    delete_parametros_confim,
)
from src.module.parametros.service import Service
from src.module.parametros.model import Parametros
from src.cli.prompts import get_parametros_form
from src.module.parametros.dto import ParametrosDto


class ParametroController:
    def __init__(self):
        self.service = Service()
        create_database()

    def run(self):
        while True:
            choice = parametros_menu_prompt()

            if choice == "Voltar" or choice is None:
                break

            match choice:

                case "Criar Parametro":
                    self._handle_create_parametro()
                    break

                case "Editar Parametro":
                    self._handle_edit_parametro()
                    break

                case "Deletar":
                    self._handle_delete_parametro()
                    break

                case _:
                    break

    # =========================================
    # Utils
    # =========================================
    def get_info(self) -> dict:
        existParans = self.service.find_all()

        if len(existParans) == 0:
            return {"sigla": "-", "nome": "-", "gpa": "-", "npj": "-"}

        return {
            "sigla": existParans[0].sigla_unidade,
            "nome": existParans[0].nome_unidade,
            "gpa": existParans[0].isGPA,
            "npj": existParans[0].isNPJ,
        }

    # =========================================
    # HANDLES
    # =========================================
    def _handle_create_parametro(self):
        try:
            existParans = self.service.find_all()

            if len(existParans) > 0:
                print("Já existe parametro cadastrado")
                input()
                return

            req = get_parametros_form()

            dto = ParametrosDto(
                sigla_unidade=req["sigla"],
                nome_unidade=req["nome"],
                isGPA=req["gpa"],
                isNPJ=req["npj"],
            )

            self.service.create(dto)

            print("Parametro criado com Sucesso!")

        except Exception as err:
            print(err)

    def _handle_edit_parametro(self):
        existParans = self.service.find_all()

        if len(existParans) == 0:
            print("Não existe parametro cadastrado")
            input()
            return

        data = [
            {
                "sigla": e.sigla_unidade,
                "nome": e.nome_unidade,
                "gpa": "Sim" if e.isGPA else "Não",
                "npj": "Sim" if e.isNPJ else "Não",
            }
            for e in existParans
        ]

        req = edit_parametros_form(data[0])

        dto = ParametrosDto(
            sigla_unidade=req["sigla"],
            nome_unidade=req["nome"],
            isGPA=req["gpa"],
            isNPJ=req["npj"],
        )

        result = self.service.edit(id=existParans[0].id, paramDto=dto)

        if result is None:
            print("Error ao editar Parametro")
            input()

            return

        print("Parametro editado com sucesso!")

    def _handle_delete_parametro(self):
        existParans = self.service.find_all()

        if len(existParans) == 0:
            print("Não existe parametro cadastrado")
            input()
            return

        result = delete_parametros_confim()

        if result:
            self.service.delete(id=existParans[0].id)
            print("Parametro deletado com sucesso!")
            return
