from sqlalchemy import select

from src.database.db_config import create_database, SessionLocal
from src.module.aluno.aluno_model import AlunoModel


class AlunoStorage:
    def __init__(self):
        create_database()

    #
    #
    #
    #
    def create(
        self,
        id: str,
        matricula: str,
        nome: str,
        codigo_externo: str,
        cpf: int,
        email: str,
        login: str,
        senha: str,
        isAtivo: bool,
    ) -> "AlunoModel":

        with SessionLocal() as session:

            aluno = AlunoModel(
                id=id,
                matricula=matricula,
                nome=nome,
                codigo_externo=codigo_externo,
                cpf=cpf,
                email=email,
                login=login,
                senha=senha,
                isAtivo=isAtivo,
            )

            session.add(aluno)
            session.commit()

            session.refresh(aluno)

            return aluno

    #
    #
    #
    #
    def update(
        self,
        id: str,
        matricula: str,
        nome: str,
        codigo_externo: str,
        cpf: int,
        email: str,
        login: str,
        senha: str,
        isAtivo: bool,
    ) -> "AlunoModel":

        with SessionLocal() as session:

            aluno = session.get(AlunoModel, id)

            if not aluno:
                return None

            aluno.matricula = matricula
            aluno.nome = nome
            aluno.codigo_externo = codigo_externo
            aluno.cpf = cpf
            aluno.email = email
            aluno.login = login
            aluno.senha = senha
            aluno.isAtivo = isAtivo

            session.commit()
            session.refresh(aluno)

            return aluno

    #
    #
    #
    #
    def find_all(self) -> list["AlunoModel"]:
        with SessionLocal() as session:

            statement = select(AlunoModel)

            alunos = session.scalars(statement).all()

            return alunos

    #
    #
    #
    #
    def find_by_id(self, id: str) -> "AlunoModel":

        with SessionLocal() as session:
            return session.get(AlunoModel, id)

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

    #
    #
    #
    #
    def find_by_cod_externo(self, codigo_externo: str) -> "AlunoModel":

        with SessionLocal() as session:
            statement = select(AlunoModel).where(
                AlunoModel.codigo_externo == codigo_externo
            )

            relogio = session.scalar(statement)

            return relogio
