from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base

if TYPE_CHECKING:
    from src.models.user import User


class Address(Base):
    """Model of the public.addresses table.

    Attributes:
        city (str): City of the address.
        country (str): Country of the address.
        number (str): House number of the address.
        postcode (str): Postal code of the address.
        street_name (str): Street name of the address.
        user_id (int): Unique identifier of the user.
    """

    __tablename__ = "addresses"

    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    number: Mapped[str] = mapped_column(String(10), nullable=False)
    postcode: Mapped[str] = mapped_column(String(20), nullable=False)
    street_name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    # Relationship to user
    user: Mapped["User"] = relationship("User", back_populates="address")
