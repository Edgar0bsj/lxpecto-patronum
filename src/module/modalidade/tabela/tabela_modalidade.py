from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Input


class ModalidadeTable(App):
    def sett_data(self, data: list):
        self.dados_originais = data

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Buscar...")
        yield DataTable()

    #
    #
    #
    #
    #
    #
    # -------------------------------------------------------------
    # Montando a tabela
    # -------------------------------------------------------------
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Nome", "Codigo", "Tipo Modalidade")

        self.atualizar_tabela(self.dados_originais)

    #
    #
    #
    #
    #
    #
    # -------------------------------------------------------------
    # Atualizando tabela
    # -------------------------------------------------------------
    def atualizar_tabela(self, linhas: list) -> None:
        table = self.query_one(DataTable)
        table.clear()
        for linha in linhas:
            table.add_row(*linha)

    #
    #
    #
    #
    #
    #
    # -------------------------------------------------------------
    # Filtro ao Digitar
    # -------------------------------------------------------------
    @on(Input.Changed)
    def ao_digitar_no_filtro(self, event: Input.Changed) -> None:
        texto_busca = event.value.strip().lower()

        if not texto_busca:
            self.atualizar_tabela(self.dados_originais)
            return

        dados_filtrados = [
            linha
            for linha in self.dados_originais
            if any(texto_busca in str(campo).lower() for campo in linha)
        ]

        self.atualizar_tabela(dados_filtrados)

    #
    #
    #
    #
    #
    #
    # -------------------------------------------------------------
    # Quando der Enter no Input, passa o foco direto para a DataTable
    # -------------------------------------------------------------

    @on(Input.Submitted)
    def ao_pressionar_enter_no_input(self, event: Input.Submitted) -> None:
        self.query_one(DataTable).focus()

    #
    #
    #
    #
    #
    #
    # -------------------------------------------------------------
    # Exibe notificação visível na interface do Textual
    # -------------------------------------------------------------
    def processar_modalidade(self, nome: str, codigo: str, tipo: str) -> None:
        self.notify(
            message=f"Código: {codigo} | Tipo: {tipo}",
            title=f"Modalidade Selecionada: {nome}",
            severity="information",
        )

    #
    #
    #
    #
    #
    #
    # -------------------------------------------------------------
    # Captura o Enter quando a DataTable estiver em foco
    # -------------------------------------------------------------

    @on(DataTable.RowSelected)
    def ao_selecionar_linha(self, event: DataTable.RowSelected) -> None:
        table = event.data_table
        linha_dados = table.get_row(event.row_key)

        nome, codigo, tipo = linha_dados
        self.processar_modalidade(nome, codigo, tipo)


#
#
#
#
#
#
# -------------------------------------------------------------
# Testando a Tabela :D
# -------------------------------------------------------------
if __name__ == "__main__":
    data = [
        ("Presencial", "MOD-001", "PRESENCIAL"),
        ("Semi-presencial", "MOD-002", "HIBRIDO"),
        ("EAD 100% Online", "MOD-003", "DISTANCIA"),
    ]

    app = ModalidadeTable()
    app.sett_data(data)
    app.run()
