from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import DATE, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.models.address import Address


class User(Base):
    """Model for the public.users table.

    Attributes:
        date_of_birth (datetime.date): When the user was born.
        firstname (str): The first name of the user.
        id (int): Unique identifier of the user.
        lastname (str): The last name of the user.
    """

    __tablename__ = "users"

    date_of_birth: Mapped[date] = mapped_column(DATE, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationship to address (one-to-one)
    address: Mapped["Address"] = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan", uselist=True, lazy="selectin"
    )
