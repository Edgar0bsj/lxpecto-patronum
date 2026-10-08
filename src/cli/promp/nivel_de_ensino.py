import questionary


def nivel_de_ensino_menu_prompt() -> str:
    return questionary.select(
        "=== NIVEL DE ENSINO ===",
        instruction=" ",
        choices=[
            "Visualizar Nivel de Ensino",
            "Baixar Modelo em Branco (.xlsx)",
            "Importar Dados do Excel",
            "Exportar Dados Cadastrados",
            "Excluir Nivel de Ensino",
            "Voltar ao Menu Principal",
        ],
    ).ask()


def file_path_prompt() -> str:
    return questionary.path("Deve ser .xlsx (excel)").ask()
