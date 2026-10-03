from sqlalchemy import func, select

from src.module.modalidade.model import Modalidade
from src.module.modalidade.dto import ModalidadeDto
from src.database.database import create_database, SessionLocal


class Repository:
    def __init__(self):
        create_database()

    def save(self, modDto: ModalidadeDto) -> "Modalidade":

        with SessionLocal() as session:

            mod = Modalidade(
                nome=modDto.nome,
                codigo=modDto.codigo,
                tipo_modalidade=modDto.tipo_modalidade,
            )

            session.add(mod)
            session.commit()

            session.refresh(mod)

            return mod

    def find_all(self) -> list["Modalidade"]:
        with SessionLocal() as session:

            statement = select(Modalidade)

            parans = session.scalars(statement).all()

            return parans

    def find_by_id(self, id: int) -> "Modalidade":

        with SessionLocal() as session:
            return session.get(Modalidade, id)

    def edit(self, modDto: ModalidadeDto) -> "Modalidade":

        with SessionLocal() as session:

            mod = session.get(Modalidade, modDto.id)

            if not mod:
                return None

            mod.nome = modDto.nome
            mod.codigo = modDto.codigo
            mod.tipo_modalidade = modDto.tipo_modalidade

            session.commit()
            session.refresh(mod)

            return mod

    def delete(self, id: int) -> bool:

        with SessionLocal() as session:

            entity = session.get(Modalidade, id)

            if not entity:
                return False

            session.delete(entity)
            session.commit()

            return True

    def find_by_cod(self, cod: str) -> "Modalidade":

        with SessionLocal() as session:
            statement = select(Modalidade).where(Modalidade.codigo == cod)

            mod = session.scalar(statement)

            return mod

    def find_by_last_update(self):

        with SessionLocal() as session:
            latest_update = session.query(func.max(Modalidade.updated_at)).scalar()

            return latest_update
