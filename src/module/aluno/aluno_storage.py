from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.db_config import SessionLocal, create_database
from src.module.aluno.aluno_dto import AlunoFiltro
from src.module.aluno.aluno_model import AlunoModel


class AlunoStorage:
    def __init__(self):
        create_database()

    # =============================================
    # CREATED
    # =============================================
    def save(self, aluno_model: AlunoModel) -> None:

        with SessionLocal() as session:

            session.add(aluno_model)
            session.commit()

            session.refresh(aluno_model)

            return aluno_model

    # =============================================
    # UPDATED
    # =============================================
    def update(self, id: str, aluno_model: AlunoModel) -> None:

        with SessionLocal() as session:
            aluno = session.get(AlunoModel, id)

            aluno.nome = aluno_model.nome
            aluno.cpf = aluno_model.cpf

            session.commit()
            session.refresh(aluno)

            return aluno

    # =============================================
    # FIND ALL
    # =============================================
    def find_all(self, aluno_filtro: AlunoFiltro) -> list["AlunoModel"]:
        with SessionLocal() as session:

            statement = select(AlunoModel).options(selectinload(AlunoModel.vinculo))

            if aluno_filtro.nome:
                statement = statement.where(
                    AlunoModel.nome.ilike(f"%{aluno_filtro.nome}%")
                )

            if aluno_filtro.cpf:
                statement = statement.where(
                    AlunoModel.cpf.ilike(f"%{aluno_filtro.cpf}%")
                )

            alunos = session.scalars(statement).all()

            return alunos

    # =============================================
    # FIND BY ID
    # =============================================
    def find_by_id(self, id: str) -> "AlunoModel":

        with SessionLocal() as session:

            statement = (
                select(AlunoModel)
                .where(AlunoModel.id == id)
                .options(selectinload(AlunoModel.vinculo))
            )

            aluno = session.scalars(statement).first()

            return aluno

    # =============================================
    # DELETED
    # =============================================
    def delete(self, id: str) -> bool:

        with SessionLocal() as session:

            entity = session.get(AlunoModel, id)

            if not entity:
                return False

            session.delete(entity)
            session.commit()

            return True

    # =============================================
    # FIND BY CPF
    # =============================================
    def find_by_cpf(self, cpf: str) -> "AlunoModel":

        with SessionLocal() as session:

            statement = (
                select(AlunoModel)
                .where(AlunoModel.cpf == cpf)
                .options(selectinload(AlunoModel.vinculo))
            )

            aluno = session.scalars(statement).first()

            return aluno
