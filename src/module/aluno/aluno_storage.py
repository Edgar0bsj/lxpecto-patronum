from sqlalchemy import select

from src.module.aluno.aluno_dto import AlunoFiltro
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
    def find_all(self, aluno_filtro: AlunoFiltro) -> list["AlunoModel"]:
        with SessionLocal() as session:

            statement = select(AlunoModel)
            if aluno_filtro.matricula:
                statement = statement.where(
                    AlunoModel.matricula.ilike(f"%{aluno_filtro.matricula}%")
                )

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

            if aluno_filtro.email:
                statement = statement.where(
                    AlunoModel.email.ilike(f"%{aluno_filtro.email}%")
                )

            if aluno_filtro.login:
                statement = statement.where(
                    AlunoModel.login.ilike(f"%{aluno_filtro.login}%")
                )

            if aluno_filtro.isAtivo is not None:
                statement = select(AlunoModel).where(
                    AlunoModel.isAtivo == aluno_filtro.isAtivo
                )

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

            aluno = session.scalar(statement)

            return aluno

    #
    #
    #
    #
    def find_by_nome(self, nome: str) -> list["AlunoModel"]:

        with SessionLocal() as session:
            statement = select(AlunoModel).where(AlunoModel.nome.ilike(f"%{nome}%"))

            alunos = session.scalars(statement).all()

            return alunos
