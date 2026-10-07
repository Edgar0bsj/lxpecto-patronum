from sqlalchemy import select

from src.database.database import SessionLocal
from src.module.parametros.model import Parametros
from src.module.parametros.dto import ParametrosDto


class Repository:

    @staticmethod
    def save(entityDto: ParametrosDto) -> Parametros:

        with SessionLocal() as session:

            parametros = Parametros(
                sigla_unidade=entityDto.sigla_unidade,
                nome_unidade=entityDto.nome_unidade,
                isGPA=entityDto.isGPA,
                isNPJ=entityDto.isNPJ,
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

    @staticmethod
    def edit(id: int, entityDto: ParametrosDto) -> Parametros | None:

        with SessionLocal() as session:

            param = session.get(Parametros, id)

            if not param:
                return None

            param.sigla_unidade = entityDto.sigla_unidade
            param.nome_unidade = entityDto.nome_unidade
            param.isGPA = entityDto.isGPA
            param.isNPJ = entityDto.isNPJ

            session.commit()
            session.refresh(param)

            return param

    @staticmethod
    def delete(id: int) -> bool:

        with SessionLocal() as session:

            entity = session.get(Parametros, id)

            if not entity:
                return False

            session.delete(entity)
            session.commit()

            return True
