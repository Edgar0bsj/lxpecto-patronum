from nanoid import generate

from src.module.vinculo.vinculo_storage import VinculoStorage


class VinculoService:
    def __init__(self):
        self.repo = VinculoStorage()

    # =============================================
    # Gerar Id
    # =============================================
    def generate_id(self, prefixo: str = ""):
        token = generate(size=17)

        id = f"vinc_{prefixo}{token}"

        return id
