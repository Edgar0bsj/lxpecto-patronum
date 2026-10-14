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
                modalidade=vinculo_dto.modalidade.value,
                polo=vinculo_dto.polo.value,
                email=vinculo_dto.email,
                status=vinculo_dto.status,
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
            vinculo.modalidade = vinculo_dto.modalidade.value
            vinculo.polo = vinculo_dto.polo.value
            vinculo.email = vinculo_dto.email
            vinculo.status = vinculo_dto.status
            aluno_id = (vinculo_dto.aluno_id,)

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

            if vinculo_filtro.modalidade:
                statement = statement.where(
                    VinculoModel.modalidade.ilike(
                        f"%{vinculo_filtro.modalidade.value}%"
                    )
                )

            if vinculo_filtro.polo:
                statement = statement.where(
                    VinculoModel.polo.ilike(f"%{vinculo_filtro.polo.value}%")
                )

            if vinculo_filtro.email:
                statement = statement.where(
                    VinculoModel.email.ilike(f"%{vinculo_filtro.email}%")
                )

            if vinculo_filtro.status is not None:
                statement = select(VinculoModel).where(
                    VinculoModel.status == vinculo_filtro.status
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
