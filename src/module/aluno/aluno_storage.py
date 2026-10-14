from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.module.aluno.aluno_dto import AlunoFiltro, AlunoRequest
from src.database.db_config import create_database, SessionLocal
from src.module.aluno.aluno_model import AlunoModel


class AlunoStorage:
    def __init__(self):
        create_database()

    #
    #
    #
    #
    def create(self, id: str, aluno_dto: AlunoRequest) -> "AlunoModel":

        with SessionLocal() as session:

            aluno = AlunoModel(
                id=id,
                nome=aluno_dto.nome,
                codigo_externo=aluno_dto.cpf,
                cpf=aluno_dto.cpf,
                login=aluno_dto.login,
                senha=aluno_dto.senha,
            )

            session.add(aluno)
            session.commit()

            session.refresh(aluno)

            return aluno

    #
    #
    #
    #
    def update(self, id: str, aluno_dto: AlunoRequest) -> "AlunoModel":

        with SessionLocal() as session:

            aluno = session.get(AlunoModel, id)

            if not aluno:
                return None

            aluno.nome = aluno_dto.nome
            aluno.codigo_externo = aluno_dto.codigo_externo
            aluno.cpf = aluno_dto.cpf
            aluno.login = aluno_dto.login
            aluno.senha = aluno_dto.senha

            session.commit()
            session.refresh(aluno)

            return aluno

    #
    #
    #
    #
    def find_all(self, aluno_filtro: AlunoFiltro) -> list["AlunoModel"]:
        with SessionLocal() as session:

            statement = select(AlunoModel).options(selectinload(AlunoModel.vinculo))

            if aluno_filtro.nome:
                statement = statement.where(
                    AlunoModel.nome.ilike(f"%{aluno_filtro.nome}%")
                )

            if aluno_filtro.codigo_externo:
                statement = statement.where(
                    AlunoModel.codigo_externo.ilike(f"%{aluno_filtro.codigo_externo}%")
                )

            if aluno_filtro.cpf:
                statement = statement.where(
                    AlunoModel.cpf.ilike(f"%{aluno_filtro.cpf}%")
                )

            if aluno_filtro.login:
                statement = statement.where(
                    AlunoModel.login.ilike(f"%{aluno_filtro.login}%")
                )

            alunos = session.scalars(statement).all()

            return alunos

    #
    #
    #
    #
    def find_by_id(self, id: str) -> "AlunoModel":

        with SessionLocal() as session:

            statement = (
                select(AlunoModel)
                .options(selectinload(AlunoModel.vinculo))
                .where(AlunoModel.id == id)
            )

            aluno = session.scalars(statement).first()

            return aluno

    #
    #
    #
    #
    def delete(self, id: str) -> bool:

        with SessionLocal() as session:

            entity = session.get(AlunoModel, id)

            if not entity:
                return False

            session.delete(entity)
            session.commit()

            return True
