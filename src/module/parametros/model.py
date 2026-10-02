from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Parametros(Base):
    __tablename__ = "parametros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    sigla_unidade: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    nome_unidade: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    isGPA: Mapped[bool] = mapped_column(Boolean, default=False)

    isNPJ: Mapped[bool] = mapped_column(Boolean, default=False)
