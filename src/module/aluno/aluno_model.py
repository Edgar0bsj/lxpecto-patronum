from src.database.db_config import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Boolean


class AlunoModel(Base):
    __tablename__ = "aluno"

    id: Mapped[str] = mapped_column(primary_key=True)

    nome: Mapped[str] = mapped_column(String(150), nullable=False)

    codigo_externo: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True
    )

    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)

    login: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    senha: Mapped[str] = mapped_column(String(100), nullable=True)

    #
    #
    # Relacionamento Vinculo
    vinculo: Mapped[list["VinculoModel"]] = relationship(  # type: ignore
        back_populates="aluno", cascade="all"
    )
    # ================
    #
    #

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
