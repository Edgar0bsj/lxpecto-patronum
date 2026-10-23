from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.db_config import SessionLocal, create_database
from src.module.vinculo.vinculo_dto import VinculoFiltro
from src.module.vinculo.vinculo_model import VinculoModel


class VinculoStorage:
    def __init__(self):
        create_database()

    # =============================================
    # CREATED
    # =============================================
    def save(self, vinculo_model: VinculoModel) -> None:

        with SessionLocal() as session:

            session.add(vinculo_model)
            session.commit()

            session.refresh(vinculo_model)

            return vinculo_model

    # =============================================
    # UPDATED
    # =============================================
    def update(self, id: str, vinculo_model: VinculoModel) -> None:

        with SessionLocal() as session:

            vinculo = session.get(VinculoModel, id)

            vinculo.matricula = vinculo_model.matricula
            vinculo.email = vinculo_model.email
            vinculo.status = vinculo_model.status
            vinculo.login = vinculo_model.login
            vinculo.senha = vinculo_model.senha
            vinculo.is_primary = vinculo_model.is_primary
            vinculo.tags = vinculo_model.tags
            vinculo.aluno_id = vinculo_model.aluno_id

            session.commit()
            session.refresh(vinculo)

            return vinculo

    # =============================================
    # FIND ALL
    # =============================================
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

            if vinculo_filtro.tags:
                statement = statement.where(
                    VinculoModel.tags.ilike(f"%{vinculo_filtro.tags}%")
                )

            vinculo = session.scalars(statement).all()

            return vinculo

    # =============================================
    # FIND BY ID
    # =============================================
    def find_by_id(self, id: str) -> "VinculoModel":

        with SessionLocal() as session:

            statement = (
                select(VinculoModel)
                .where(VinculoModel.id == id)
                .options(selectinload(VinculoModel.aluno))
            )

            vinculos = session.scalars(statement).first()
            return vinculos

    # =============================================
    # DELETED
    # =============================================
    def delete(self, id: str) -> bool:

        with SessionLocal() as session:

            entity = session.get(VinculoModel, id)

            if not entity:
                return False

            session.delete(entity)
            session.commit()

            return True

    # =============================================
    # IS EXIST
    # =============================================
    def is_exist(
        self,
        *,
        matricula: str | None = None,
        email: str | None = None,
        login: str | None = None,
    ) -> bool:
        with SessionLocal() as session:

            statement = select(VinculoModel)

            if matricula:
                statement = statement.where(VinculoModel.matricula == matricula)
            if email:
                statement = statement.where(VinculoModel.email == email)
            if login:
                statement = statement.where(VinculoModel.login == login)

            statement = statement.limit(1)
            existe = session.scalar(statement)

            return bool(existe)
