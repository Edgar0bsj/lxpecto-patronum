from dataclasses import dataclass, fields, is_dataclass
from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Input


class DynamicTableApp(App):

    def __init__(self, data: list[Any]):
        super().__init__()
        self.data = data

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Digite para buscar...")
        yield DataTable()

    def on_mount(self) -> None:
        if not self.data:
            return

        table = self.query_one(DataTable)

        # 1. Extrai dinamicamente as colunas do primeiro item da lista
        headers = self._extract_headers(self.data[0])
        table.add_columns(*headers)

        # 2. Renderiza os dados iniciais
        self._populate_table(self.data)

    def _extract_headers(self, item: Any) -> list[str]:
        """Identifica os nomes das colunas com base no tipo do objeto."""
        if isinstance(item, dict):
            return [str(k).upper() for k in item.keys()]
        if is_dataclass(item):
            return [f.name.upper() for f in fields(item)]
        if hasattr(item, "__dict__"):
            return [k.upper() for k in vars(item).keys() if not k.startswith("_")]
        return ["VALOR"]

    def _extract_row_values(self, item: Any) -> list[str]:
        """Converte as propriedades do objeto em uma lista de strings para a tabela."""
        if isinstance(item, dict):
            return [str(v) for v in item.values()]
        if is_dataclass(item):
            return [str(getattr(item, f.name)) for f in fields(item)]
        if hasattr(item, "__dict__"):
            return [str(v) for k, v in vars(item).items() if not k.startswith("_")]
        return [str(item)]

    def _populate_table(self, items: list[Any]) -> None:
        table = self.query_one(DataTable)
        table.clear()
        for item in items:
            row = self._extract_row_values(item)
            table.add_row(*row)

    def on_input_changed(self, event: Input.Changed) -> None:
        """Filtro dinâmico em tempo real."""
        query = event.value.lower()
        if not query:
            self._populate_table(self.data)
            return

        filtered = [
            item
            for item in self.data
            if any(query in str(val).lower() for val in self._extract_row_values(item))
        ]
        self._populate_table(filtered)


if __name__ == "__main__":
    objs = [{"nome": "edgar", "idade": 27}, {"nome": "marcelo", "idade": 12}]
    DynamicTableApp(data=objs).run()
