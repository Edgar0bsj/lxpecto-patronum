import questionary


def modalidade_menu_prompt() -> str:
    return questionary.select(
        "=== MODALIDADE ===",
        instruction=" ",
        choices=[
            "Visualizar Modalidades",
            "Baixar Modelo em Branco (.xlsx)",
            "Importar Dados do Excel",
            "Exportar Dados Cadastrados",
            "Excluir Dados via Excel",
            "Voltar ao Menu Principal",
        ],
    ).ask()


def file_path_prompt() -> str:
    return questionary.path("Deve ser .xlsx (excel)").ask()
