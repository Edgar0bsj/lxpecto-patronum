from src.database.db_config import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime, String


class AlunoModel(Base):
    __tablename__ = "aluno"

    id: Mapped[str] = mapped_column(primary_key=True, unique=True)

    nome: Mapped[str] = mapped_column(String(150), nullable=False)

    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)

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
