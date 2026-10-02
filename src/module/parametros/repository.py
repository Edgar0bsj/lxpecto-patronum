from sqlalchemy import select

from src.database.database import SessionLocal
from src.module.parametros.model import Parametros
from src.module.parametros.dto import ParametrosDto


class Repository:

    @staticmethod
    def save(entity: ParametrosDto) -> Parametros:

        with SessionLocal() as session:

            parametros = Parametros(
                sigla_unidade=entity.sigla_unidade,
                nome_unidade=entity.nome_unidade,
                isGPA=entity.isGPA,
                isNPJ=entity.isNPJ,
            )

            session.add(parametros)
            session.commit()

            session.refresh(parametros)

            return parametros

    @staticmethod
    def find_all() -> list[Parametros]:

        with SessionLocal() as session:

            statement = select(Parametros)

            parans = session.scalars(statement).all()

            return parans
