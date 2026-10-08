from sqlalchemy import func, select

from src.module.niveis_ensino.domain import NivelDeEnsino
from src.module.niveis_ensino.dto import NivelDeEnsinoDto
from src.database.database import create_database, SessionLocal


class Repository:
    def __init__(self):
        create_database()

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def save(self, ndeDto: NivelDeEnsinoDto) -> "NivelDeEnsinoDto":

        with SessionLocal() as session:

            nde = NivelDeEnsino(
                nome=ndeDto.nome, codigo=ndeDto.codigo, tipo_nivel=ndeDto.tipo_de_nivel
            )

            session.add(nde)
            session.commit()

            session.refresh(nde)

            return nde

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def find_all(self) -> list["NivelDeEnsino"]:
        with SessionLocal() as session:

            statement = select(NivelDeEnsino)

            parans = session.scalars(statement).all()

            return parans

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def find_by_id(self, id: int) -> "NivelDeEnsino":

        with SessionLocal() as session:
            return session.get(NivelDeEnsino, id)

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def edit(self, ndeDto: NivelDeEnsinoDto) -> "NivelDeEnsino":

        with SessionLocal() as session:

            nde = session.get(NivelDeEnsino, ndeDto.id)

            if not nde:
                return None

            nde.nome = ndeDto.nome
            nde.codigo = ndeDto.codigo
            nde.tipo_de_nivel = ndeDto.tipo_de_nivel

            session.commit()
            session.refresh(nde)

            return nde

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def delete(self, id: int) -> bool:

        with SessionLocal() as session:

            entity = session.get(NivelDeEnsino, id)

            if not entity:
                return False

            session.delete(entity)
            session.commit()

            return True

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def find_by_cod(self, cod: str) -> "NivelDeEnsino":

        with SessionLocal() as session:
            statement = select(NivelDeEnsino).where(NivelDeEnsino.codigo == cod)

            nde = session.scalar(statement)

            return nde

    #
    #
    #
    #
    #
    #
    #
    #
    #

    def find_by_last_update(self):

        with SessionLocal() as session:
            latest_update = session.query(func.max(NivelDeEnsino.updated_at)).scalar()

            return latest_update
