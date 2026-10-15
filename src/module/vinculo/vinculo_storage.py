from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.module.vinculo.vinculo_dto import VinculoDto, VinculoFiltro

from src.database.db_config import create_database, SessionLocal
from src.module.vinculo.vinculo_model import VinculoModel


class VinculoStorage:
    def __init__(self):
        create_database()

    #
    #
    #
    #
    def create(self, id: str, vinculo_dto: VinculoDto) -> "VinculoModel":

        with SessionLocal() as session:

            vinculo = VinculoModel(
                id=id,
                matricula=vinculo_dto.matricula,
                email=vinculo_dto.email,
                status=vinculo_dto.status,
                login=vinculo_dto.login,
                senha=vinculo_dto.senha,
                is_primary=vinculo_dto.is_primary,
                aluno_id=vinculo_dto.aluno_id,
            )

            session.add(vinculo)
            session.commit()

            session.refresh(vinculo)

            return vinculo

    #
    #
    #
    #
    def update(self, id: str, vinculo_dto: VinculoDto) -> "VinculoModel":

        with SessionLocal() as session:

            vinculo = session.get(VinculoModel, id)

            if not vinculo:
                return None

            vinculo.matricula = vinculo_dto.matricula
            vinculo.email = vinculo_dto.email
            vinculo.status = vinculo_dto.status
            vinculo.login = vinculo_dto.login
            vinculo.senha = vinculo_dto.senha
            vinculo.is_primary = vinculo_dto.is_primary
            vinculo.aluno_id = vinculo_dto.aluno_id

            session.commit()
            session.refresh(vinculo)

            return vinculo

    #
    #
    #
    #
    def find_all(self, vinculo_filtro: VinculoFiltro) -> list["VinculoModel"]:
        with SessionLocal() as session:

            statement = select(VinculoModel).options(selectinload(VinculoModel.aluno))

            if vinculo_filtro.matricula:
                statement = statement.where(
                    VinculoModel.matricula.ilike(f"%{vinculo_filtro.matricula}%")
                )

            if vinculo_filtro.email:
                statement = statement.where(
                    VinculoModel.email.ilike(f"%{vinculo_filtro.email}%")
                )

            if vinculo_filtro.status is not None:
                statement = statement.where(
                    VinculoModel.status == vinculo_filtro.status
                )

            if vinculo_filtro.login:
                statement = statement.where(
                    VinculoModel.login.ilike(f"%{vinculo_filtro.login}%")
                )

            if vinculo_filtro.is_primary is not None:
                statement = statement.where(
                    VinculoModel.is_primary == vinculo_filtro.is_primary
                )

            if vinculo_filtro.aluno_id:
                statement = statement.where(
                    VinculoModel.aluno_id.ilike(f"%{vinculo_filtro.aluno_id}%")
                )

            vinculo = session.scalars(statement).all()

            return vinculo

    #
    #
    #
    #
    def find_by_id(self, id: str) -> "VinculoModel":

        with SessionLocal() as session:
            return session.get(VinculoModel, id)

    #
    #
    #
    #
    def delete(self, id: str) -> bool:

        with SessionLocal() as session:

            entity = session.get(VinculoModel, id)

            if not entity:
                return False

            session.delete(entity)
            session.commit()

            return True
