from src.database.db_config import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import DateTime, String, Boolean


class VinculoModel(Base):
    __tablename__ = "vinculo"

    id: Mapped[str] = mapped_column(primary_key=True)

    matricula: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    modalidade: Mapped[str] = mapped_column(String(100), nullable=False)

    polo: Mapped[str] = mapped_column(String(50), nullable=False)

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    status: Mapped[bool] = mapped_column(Boolean, default=False)
    #
    #
    # Relacionamento
    aluno_id: Mapped[str] = mapped_column(ForeignKey("aluno.id"), nullable=False)
    aluno: Mapped["AlunoModel"] = relationship(back_populates="vinculo")  # type: ignore
    # ================
    #
    #
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
