import questionary


def main_menu_prompt() -> str:
    return questionary.select(
        "-- MENU --",
        instruction=" ",
        choices=["Parametros", "Sair"],
    ).ask()


# =======================================
# PARAMETROS
# =======================================
def parametros_menu_prompt() -> str:
    return questionary.select(
        "=== PARAMETROS ===",
        instruction=" ",
        choices=[
            "Criar Parametro",
            "Editar Parametro",
            "Deletar",
            "Voltar",
        ],
    ).ask()


def get_parametros_form() -> dict:
    sigla = questionary.text("Sigla da unidade:").ask()
    nome = questionary.text("Nome da unidade:").ask()
    gpa = questionary.select("GPA ?:", choices=["Sim", "Não"], instruction=" ").ask()
    npj = questionary.select("NPJ ?:", choices=["Sim", "Não"], instruction=" ").ask()

    sigla = str(sigla)
    nome = str(nome)
    gpa = True if gpa == "Sim" else False
    npj = True if npj == "Sim" else False

    return {
        "sigla": sigla,
        "nome": nome,
        "gpa": gpa,
        "npj": npj,
    }


def edit_parametros_form(data: dict) -> dict:
    sigla = questionary.text("Sigla da unidade:", default=data["sigla"]).ask()
    nome = questionary.text("Nome da unidade:", default=data["nome"]).ask()
    gpa = questionary.select(
        "GPA ?:", choices=["Sim", "Não"], instruction=" ", default=data["gpa"]
    ).ask()
    npj = questionary.select(
        "NPJ ?:", choices=["Sim", "Não"], instruction=" ", default=data["npj"]
    ).ask()

    sigla = str(sigla)
    nome = str(nome)
    gpa = True if gpa == "Sim" else False
    npj = True if npj == "Sim" else False

    return {
        "sigla": sigla,
        "nome": nome,
        "gpa": gpa,
        "npj": npj,
    }


def delete_parametros_confim() -> bool:
    result = questionary.select(
        "Certeza ?:", choices=["Sim", "Não"], instruction=" "
    ).ask()

    result = True if result == "Sim" else False

    return result
