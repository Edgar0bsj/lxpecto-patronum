import questionary


def modalidade_menu_prompt() -> str:
    return questionary.select(
        "=== MODALIDADE ===",
        instruction=" ",
        choices=[
            "Importar via Excel",
            "Deletar via Excel",
            "Exportar em Excel",
            "Voltar",
        ],
    ).ask()


def file_path_prompt() -> str:
    return questionary.path("Deve ser .xlsx (excel)").ask()
